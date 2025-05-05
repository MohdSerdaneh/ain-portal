from django.urls import path
from . import views

urlpatterns = [
    path('live-status/<str:room_name>/', views.live_status, name='live_status'),
    path('chat-history/<str:room_name>/', views.get_chat_history, name='chat_history'),
    path('send-message/<str:room_name>/', views.send_message, name='send_message'),
]
