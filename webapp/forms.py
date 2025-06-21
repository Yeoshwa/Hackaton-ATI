from django import forms
from clean_app.models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['latitude', 'longitude', 'photo', 'description', 'gravite']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
