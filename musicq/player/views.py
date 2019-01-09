from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
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
