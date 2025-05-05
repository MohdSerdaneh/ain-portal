from django.urls import path
from . import views

# URL routes for the meeting app (video, chat, ASL polling)
urlpatterns = [
    # 🎥 Video Meeting Lobby (teacher and student routes)
    path('teacher/courses/join_meeting/<str:name>', views.lobby),
    path('student/dashboard/join_meeting/<str:name>', views.lobby),

    # 🎥 Basic room view (fallback)
    path('room/', views.room),

    # 🔐 Agora token generation for real-time video authentication
    path('get_token/', views.getToken),

    # 👤 Room member management
    path('create_member/', views.createMember),
    path('get_member/', views.getMember),
    path('delete_member/', views.deleteMember),

    # 💬 Real-time chat endpoints
    path('chat/send/', views.send_chat_message, name='send_chat_message'),
    path('chat/messages/<str:username>/', views.get_chat_messages, name='get_chat_messages'),

    # 🧠 ASL Recognition sentence polling (via shared .txt file)
    path('get-asl-sentence/', views.get_live_asl_sentence, name='get_asl_sentence'),
]
