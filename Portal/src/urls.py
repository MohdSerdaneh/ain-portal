from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    # Core Apps
    path('', include('accounts.urls')),         # Handles login, register, homepage, etc.
    path('student/', include("student.urls")),  # Student-specific views
    path('teacher/', include('teacher.urls')),  # Teacher dashboard, profile, courses
    path('quiz/', include('quiz.urls')),        # Quiz creation and management

    # Meeting App (ASL + Emotion + Chat)
    path('', include('meeting.urls')),          # For views like /get_token, /room
    path('meeting/', include('meeting.urls')),  # Handles nested routes like /meeting/chat/messages
    path('meeting/API/', include('meeting.API.urls')),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
