from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the 'accounts' app.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        """
        Hook to import and register signal handlers when the app is ready.
        Ensures signal connections (like auto-creating profiles) are active.
        """
        import accounts.signals  # noqa
