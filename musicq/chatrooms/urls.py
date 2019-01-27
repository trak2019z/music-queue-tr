from django.urls import path, re_path
from . import views


urlpatterns = [
    path('list/', views.RoomListView.as_view(template_name='chatrooms/chat.html'),  name='room_list'),
    path('create/', views.CreateRoomView.as_view(template_name='chatrooms/create_room.html'), name='room_create'),
    re_path(r'^delete/(?P<pk>\d+)/$', views.RoomDeleteView.as_view(template_name='chatrooms/delete_room.html'), name='room_delete'),
    re_path(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    ]