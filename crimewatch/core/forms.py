from django import forms
from .models import CrimeCase

class CrimeCaseForm(forms.ModelForm):
    class Meta:
        model = CrimeCase
        fields = ['title', 'description', 'date_occurred', 'location', 'is_solved', 'crime_type', 'categories']
        widgets = {
            'date_occurred': forms.DateInput(attrs={'type': 'date'}),
            'categories': forms.CheckboxSelectMultiple(),
        }