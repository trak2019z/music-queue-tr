from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib import messages
import json
from .models import Room, ChatMessage

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        room1 = Room.objects.filter(name=self.room_name)[0]
        message = ChatMessage.objects.create(
            author=author_user,
            room=room1,
            message=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        #'fetch_messages': fetch_messages,
        'new_message': new_message,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'room': message.room.name,
            'message': message.message,
            'created': str(message.created)

        }

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def add_song(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
