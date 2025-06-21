from django.shortcuts import render, get_object_or_404, redirect

from clean_app.models import  Report, UserProfile
import folium
from folium.plugins import MarkerCluster
from .models import Event
from .forms import ReportForm
from .forms_event import EventForm
from .forms_userprofile import UserProfileForm



def generate_map(reports, center_lat=None, center_lon=None):
    # Permet de prendre en entrée une liste d'objets Report ou de dictionnaires
    def get_attr(report, attr):
        if isinstance(report, dict):
            return report.get(attr)
        return getattr(report, attr, None)

    # Toujours centrer sur Kinshasa par défaut, sauf si coordonnées utilisateur fournies
    default_lat, default_lon = -4.325, 15.322
    if center_lat is not None and center_lon is not None:
        avg_lat, avg_lon = center_lat, center_lon
        zoom = 16  # Zoom plus élevé pour voir les rues de Kinshasa
    else:
        avg_lat, avg_lon = default_lat, default_lon
        zoom = 15  # Zoom plus élevé pour Kinshasa
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=zoom)

    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers to the map
    for report in reports:
        lat = get_attr(report, 'latitude')
        lon = get_attr(report, 'longitude')
        desc = get_attr(report, 'description')
        statut = get_attr(report, 'statut')
        photo = get_attr(report, 'photo')
        popup_html = f"<b>{desc}</b> - {statut}"
        if photo:
            # Correction du chemin de l'image pour MEDIA_URL
            if hasattr(photo, 'url'):
                photo_url = photo.url
            else:
                photo_url = f"/media/{photo}"
            popup_html += f'<br><img src="{photo_url}" width="150">'
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color='blue' if statut == 'signale' else 'red')
        ).add_to(marker_cluster)

    return m
# Create your views here.
def about(request):
    return render(request, 'webapp/about.html')

def carte(request):
    reports = Report.objects.all()
    # Récupérer les coordonnées de l'utilisateur si transmises en GET
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if lat and lon:
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            lat = lon = None
    else:
        lat = lon = None

    if reports:
        folium_map = generate_map(reports, center_lat=lat, center_lon=lon)
        map_html = folium_map._repr_html_()
    else:
        map_html = "<p>Aucun signalement disponible.</p>"

    return render(request, 'webapp/carte.html', {'map': map_html})

def signaler(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            if request.user.is_authenticated:
                report.user = request.user
            report.save()
            return render(request, 'webapp/signaler.html', {'form': ReportForm(), 'success': True})
    else:
        form = ReportForm()
    return render(request, 'webapp/signaler.html', {'form': form})

def classement(request):
    profils = UserProfile.objects.all().order_by('-points')[:10]  # Top 10 profils par points
    return render(request, 'webapp/classement.html', {'profils': profils})

def evenements(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'webapp/evenements.html', {'events': events})

def evenement_detail(request, id):
    event = Event.objects.get(pk=id)
    return render(request, 'webapp/evenement_detail.html', {'event': event})

def creer_evenement(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            if request.user.is_authenticated:
                event.organisateur = request.user
            else:
                event.organisateur = None  # ou gérer l'anonymous différemment
            event.save()
            return render(request, 'webapp/creer_evenement.html', {'form': EventForm(), 'success': True})
    else:
        form = EventForm()
    return render(request, 'webapp/creer_evenement.html', {'form': form})

def modifier_evenement(request, id):
    event = get_object_or_404(Event, pk=id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('evenement_detail', id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'webapp/modifier_evenement.html', {'form': form, 'event': event})

def supprimer_evenement(request, id):
    event = get_object_or_404(Event, pk=id)
    if request.method == 'POST':
        event.delete()
        return redirect('evenements')
    return render(request, 'webapp/supprimer_evenement.html', {'event': event})

def modifier_userprofile(request, user_id):
    profil = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('classement')
    else:
        form = UserProfileForm(instance=profil)
    return render(request, 'webapp/modifier_userprofile.html', {'form': form, 'profil': profil})

def supprimer_userprofile(request, user_id):
    profil = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        profil.delete()
        return redirect('classement')
    return render(request, 'webapp/supprimer_userprofile.html', {'profil': profil})