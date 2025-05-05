from django.contrib import admin

# Import the RoomMember model from the current app
from .models import RoomMember

# Register the RoomMember model to make it manageable via Django Admin
admin.site.register(RoomMember)
