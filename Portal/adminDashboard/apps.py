from django.apps import AppConfig

class AdmindashboardConfig(AppConfig):
    """
    Configuration class for the 'adminDashboard' Django app.
    This is automatically picked up by Django when listed in INSTALLED_APPS.
    """
    # Sets the default primary key type for models in this app to BigAutoField
    default_auto_field = "django.db.models.BigAutoField"

    # App label used by Django to locate this app
    name = "adminDashboard"  # This should match the folder name of the app
