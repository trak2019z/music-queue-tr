from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.contrib import messages
import json
from .models import Room


@login_required
def index(request):
    rooms = Room.objects.order_by('title')
    return render(request, 'chatrooms/chat.html', {
        'rooms': rooms,
    })

@login_required
def room(request, room_name):
    if Room.objects.filter(name=room_name).exists():
        return render(request, 'chatrooms/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': mark_safe(json.dumps(request.user.username))
        })
    else:
        messages.error(request, 'Room not exists')
        return redirect('home')
