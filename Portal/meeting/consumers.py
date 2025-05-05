import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "meeting_chat"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Load data from the message received
        data = json.loads(text_data)
        message = data["message"]
        sender = self.scope["user"]

        # If the user is authenticated, save the message to the database
        if sender and not isinstance(sender, AnonymousUser):
            ChatMessage.objects.create(sender=sender, message=message)

        # Send the message to the group (to all users in the meeting)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # Type of event
                "message": message,
                "username": sender.username if sender else "Anonymous"
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "username": event["username"]
        }))
