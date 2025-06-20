from django.contrib import admin
from .models import UserProfile, Report, Comment

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'statut', 'points')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'latitude', 'longitude', 'statut', 'gravite', 'created_at')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'report', 'content', 'created_at')

# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Comment, CommentAdmin)