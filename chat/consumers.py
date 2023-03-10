import json
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer

from .models import Message

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    # fetches last ten messages sent from models
    def fetch_messages(self, data):
        messages = Message.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages),
        }
        self.send_message(content)

    # returns the new message sent
    def new_message(self, data):
        # sender of the message
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        # creates the mew message in the database
        message = Message.objects.create(
            author=author_user,
            content=data['message']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    """
    convert messages to json format,
    and returns a list of messages
    
    """

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    # commands to handle action
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        # grab message from event
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    # sends message to WebSocket after retrieving last ten messages
    def send_message(self, message):
        self.send(text_data=json.dumps(message))
