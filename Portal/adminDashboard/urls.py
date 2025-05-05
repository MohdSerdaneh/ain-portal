from django.urls import path
from . import views

# URL patterns for the adminDashboard app
urlpatterns = [
    # Route: /adminpage/
    # View: views.admin (handles admin dashboard logic)
    # Name: 'adminpage' (used for {% url 'adminpage' %} in templates)
    path("adminpage/", views.admin, name="adminpage"),
]
