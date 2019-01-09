from django import forms
from .models import Room

class RoomRegisterForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description']