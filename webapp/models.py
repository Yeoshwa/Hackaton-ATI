from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Modèle d'événement pour la gestion des événements communautaires
class Event(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    lieu = models.CharField(max_length=255)
    organisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evenements_organises', null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='evenements_participes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
