import os
import django
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

# Initialize Django before WSGI application is loaded
django.setup()

# Get WSGI-compatible application for production servers
application = get_wsgi_application()
