from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/meeting/chat/$', consumers.ChatConsumer.as_asgi()),
]
