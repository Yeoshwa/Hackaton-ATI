from django.shortcuts import render, get_object_or_404, redirect

from clean_app.models import  Report, UserProfile
import folium
from folium.plugins import MarkerCluster
from .models import Event
from .forms import ReportForm
from .forms_event import EventForm



def generate_map(reports):
    # Permet de prendre en entrée une liste d'objets Report ou de dictionnaires
    if not reports:
        return None

    # Supporte à la fois objets et dicts
    def get_attr(report, attr):
        if isinstance(report, dict):
            return report.get(attr)
        return getattr(report, attr, None)

    avg_lat = sum(get_attr(r, 'latitude') for r in reports) / len(reports)
    avg_lon = sum(get_attr(r, 'longitude') for r in reports) / len(reports)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

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
            popup_html += f'<br><img src="{photo}" width="150">'
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color='blue' if statut == 'signale' else 'red')
        ).add_to(marker_cluster)

    return m
# Create your views here.
def index(request):
    return render(request, 'webapp/index.html')

def carte(request):
    reports = Report.objects.all()
    
    if reports:
        folium_map = generate_map(reports)
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