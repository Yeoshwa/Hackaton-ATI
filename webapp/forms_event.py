from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['titre', 'description', 'date', 'lieu']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
