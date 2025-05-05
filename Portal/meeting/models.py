from django.db import models
from django.conf import settings


class RoomMember(models.Model):
    """
    Represents a participant in a video/audio chat room.

    Fields:
    - name: User's display name.
    - uid: Unique identifier used by Agora or WebRTC to distinguish members.
    - room_name: The room the user is part of.
    - insession: Boolean to track if the member is currently in session.
    """
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=200)
    insession = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    """
    Stores chat messages sent in a public room (for record/history).

    Fields:
    - sender: The user who sent the message.
    - message: The content of the chat message.
    - room_name: The name of the room where the message was sent.
    - timestamp: When the message was sent.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meeting_chat_sent'
    )
    message = models.TextField()
    room_name = models.CharField(max_length=200, default="default_room")  # Provide a default value here
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:30]}"
