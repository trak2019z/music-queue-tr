from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.views.generic import View, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from player.models import Playlist
import json
from .models import Room
from .forms import RoomRegisterForm


class RoomListView(ListView):
    model = Room
    template_name = 'chatrooms/chat.html'
    context_object_name = 'rooms'
    ordering = ['name']


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'chatrooms/delete_room.html'
    success_url = reverse_lazy('room_list')

@login_required
def room(request, room_name):
    if Room.objects.filter(name=room_name).exists():
        return render(request, 'chatrooms/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': mark_safe(json.dumps(request.user.username)),
        })
    else:
        messages.error(request, 'Room not exists')
        return redirect('room_list')


class CreateRoomView(LoginRequiredMixin, View):
    form_class = RoomRegisterForm
    template_name = 'chatrooms/create_room.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'chatrooms/create_room.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            user = request.user
            if Room.objects.filter(name=room_name).exists():
                messages.error(request, 'Room already exists!')
                return render(request, self.template_name, {'form': form})
            room = Room.objects.create(name=room_name, description=description, created_by=user)
            if room:
                messages.success(request, 'Successfully created room')
                return redirect('room_list')
        else:
            return render(request, self.template_name, {'form': form})
