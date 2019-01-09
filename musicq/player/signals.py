from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Song
import pafy


@receiver(pre_save, sender=Song)
def create_song(sender, instance, **kwargs):
    url = instance.url
    print(instance)
    audio = pafy.new(url)
    best = audio.getbestaudio(preftype='m4a')
    instance.title = audio.title
    instance.best_url = best.url
