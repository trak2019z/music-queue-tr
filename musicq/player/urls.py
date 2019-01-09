from django.urls import path
from . import views


urlpatterns = [
    path('', views.PlaylistView.as_view(template_name='player/add_song.html'), name='add_song'),
    ]