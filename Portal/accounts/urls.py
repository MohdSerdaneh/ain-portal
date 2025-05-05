from django.urls import path

# Local view imports
from . import views

# URL patterns for the 'accounts' app
urlpatterns = [
    path("", views.index, name="index"),                        # Homepage / dashboard
    path("login/", views.login_view, name="login_view"),        # Login page
    path("register/", views.register, name="register"),         # Registration page
    path("logout/", views.logout_user, name="logout"),          # Logout user
]
