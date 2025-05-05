from django.apps import AppConfig

class QuizConfig(AppConfig):
    # Default primary key field type for models in this app
    default_auto_field = "django.db.models.BigAutoField"

    # Name of the app this configuration applies to
    name = "quiz"
