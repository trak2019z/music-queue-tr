from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from chatrooms.models import Room
from .forms import SongCreateForm
from .models import Playlist

'''def playlist(request):
    if request.method == 'POST':
        form = PlaylistCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PlaylistCreateForm()
    return render(request, 'playlist/add_song.html', {'form': form})'''


class PlaylistView(LoginRequiredMixin, CreateView):
    form_class = SongCreateForm
    success_url = '/playlist/'
    template_name = 'player/add_song.html'

    #def get_context_data(self, **kwargs):
    #    kwargs['object_list'] = Playlist.objects.order_by('timestamp')
    #    return super(PlaylistView, self).get_context_data(**kwargs)

def SongList(request, room_name):
    if Room.objects.filter(name=room_name).exists():
        playlist = Playlist.objects.filter(room__name=room_name).orfer_by('-timestamp')
        context = {
            'playlist': playlist
        }
        return render(request, 'player/song_list.html', context)
    else:
        messages.error(request, 'Room not exists')
        return redirect('room_list')

class SongListView(ListView):
    model = Playlist
    template_name = 'player/song_list.html'
    context_object_name = 'playlist'
    ordering = ['-timestamp']

    def get_queryset(self):
        return Playlist.objects.filter(room__name=self.kwargs['room_name'])