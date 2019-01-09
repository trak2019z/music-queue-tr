from django.db import models
from django.contrib.auth import get_user_model
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
    song = models.ManyToManyField(Song, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    '''def save(self, *args, **kwargs):
        url = self.song.url
        audio = pafy.new(url)
        best = audio.getbestaudio(preftype='m4a')
        self.best_url = best.url
        self.song_title = audio.title
        self.song = best.download()
        super(Playlist, self).save(*args, **kwargs)'''
