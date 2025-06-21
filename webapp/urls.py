from django.shortcuts import render
from django.urls import path, include
from . import views

urlpatterns = [
    path( 'about/', views.about, name='about' ),
    path( 'signaler/', views.signaler, name='signaler' ),
    path( 'classement/', views.classement, name='classement' ), 
    path( 'evenements/', views.evenements, name='evenements' ),
    path( 'evenements/<int:id>/', views.evenement_detail, name='evenement_detail' ),   
    path( 'creer_evenement/', views.creer_evenement, name='creer_evenement' ),
    path('api/', include('webapp.api_urls')),  # Ajout de l'API CRUD pour Event
    path('evenements/<int:id>/modifier/', views.modifier_evenement, name='modifier_evenement'),
    path('evenements/<int:id>/supprimer/', views.supprimer_evenement, name='supprimer_evenement'),
    path('classement/<int:user_id>/modifier/', views.modifier_userprofile, name='modifier_userprofile'),
    path('classement/<int:user_id>/supprimer/', views.supprimer_userprofile, name='supprimer_userprofile'),
]
