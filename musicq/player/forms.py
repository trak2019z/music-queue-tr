from django import forms
from .models import Playlist, Song


class SongCreateForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['url']