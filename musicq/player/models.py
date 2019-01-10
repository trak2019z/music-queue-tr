from django.db import models
from django.contrib.auth import get_user_model
from chatrooms.models import Room
import pafy
import youtube_dl

User = get_user_model()


class Song(models.Model):
    title = models.CharField(default='None', max_length=100)
    url = models.CharField(help_text='Song url from youtube', max_length=1000)
    best_url = models.CharField(default='None', max_length=1000)
    duration = models.IntegerField(default=0)
    song_file = models.FileField(upload_to='songs', blank=True)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    song = models.ForeignKey(Song, default=None, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, default=None, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def playlist(room_name):
        return Playlist.objects.filter(room=room_name).order_by('-timestamp')

    #def __str__(self):
    #    return self.song.title

    '''def save(self, *args, **kwargs):
        url = self.song.url
        audio = pafy.new(url)
        best = audio.getbestaudio(preftype='m4a')
        self.best_url = best.url
        self.song_title = audio.title
        self.song = best.download()
        super(Playlist, self).save(*args, **kwargs)'''
