from django import forms
from django.forms import ModelForm
from .models import Input

class InputForm(ModelForm):
    class Meta:
        model = Input
        fields = ['start_lat', 'start_long', 'end_lat', 'end_long']