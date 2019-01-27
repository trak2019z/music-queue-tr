from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.PlaylistView.as_view(template_name='player/add_song.html'), name='add_song'),
    #path('player/', name='player'),
    re_path(r'^(?P<room_name>[^/]+)/$',
            views.SongListView.as_view(template_name='player/song_list.html'), name='song_list'),
    ]