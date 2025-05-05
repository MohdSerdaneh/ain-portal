from django.apps import AppConfig

class MeetingConfig(AppConfig):
    """
    Configuration class for the 'meeting' Django app.

    This lets Django know how to initialize the app,
    and is referenced in the INSTALLED_APPS setting.
    """
    # Sets the default type for auto-generated primary keys
    default_auto_field = 'django.db.models.BigAutoField'

    # App name used for routing and configuration resolution
    name = 'meeting'
