from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, ChatMessage
from player.models import Song, Playlist
import json
import pafy

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages  = ChatMessage.last_10_messages(self.room_name)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

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

    def add_playlist_song(self, data):
        author = data['from']
        #room1 = Room.objects.filter(name=self.room_name)[0]
        url = data['message']
        if not Song.objects.filter(url=url).exists():
            audio = pafy.new(url)
            best = audio.getbestaudio(preftype='m4a')
            song = Song.objects.create(
                title=audio.title,
                url=data['message'],
                best_url=best.url,
                duration=audio.length
            )
            content = self.dodaj(song, author)
            #room = Room.objects.filter(name=self.room_name)
            #
            #
            # Tu trzeba poprawić
        else:
            song = Song.objects.filter(url=url)[0]
            content = self.dodaj(song, author)

        return self.send_chat_message(content)


    commands = {
        'fetch_messages': fetch_messages,
        'add_playlist_song': add_playlist_song,
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
            'message': message.message
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    def dodaj(self, song, author):
        try:
            room1 = Room.objects.filter(name=self.room_name)
            playlist = Playlist.objects.filter(id=room1[0]['playlist_id'])
            playlist.song.add(song)
        except:
            print('Error')
        content = {
            'command': 'new_message',
            'message': {
                'author': author,
                'message': "Dodano do playlisty %s" % song.title
            }
        }
        return content

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def song(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
