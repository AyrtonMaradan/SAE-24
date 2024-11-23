from django import forms
from .models import Capteur, Description

class CapteurForm(forms.ModelForm):
    class Meta:
        model = Capteur
        fields = '__all__'

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = Description
        fields = '__all__'