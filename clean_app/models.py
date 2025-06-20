from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Profil utilisateur lié au modèle User standard
class UserProfile(models.Model):
    STATUT_CHOICES = (
        ('citoyen', 'Citoyen'),
        ('admin', 'Administrateur'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='citoyen')
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Report(models.Model):
    STATUT_CHOICES = (
        ('signale', 'Signalé'),
        ('en_cours', 'En Cours'),
        ('nettoye', 'Nettoyé'),
    )
    GRAVITE_CHOICES = (
        (1, 'Faible'),
        (2, 'Moyenne'),
        (3, 'Élevée'),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.FloatField()
    longitude = models.FloatField()
    photo = models.ImageField(upload_to='reports/')
    description = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='signale')
    gravite = models.IntegerField(choices=GRAVITE_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Signalement {self.id}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commentaire de {self.user.username}'
