from django.urls import path, re_path
from . import views


urlpatterns = [
    #path('', views.index,  name='chatrooms'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    path('create_room/', views.CreateRoomView.as_view(template_name='create_room.html'), name='create_room'),
    ]