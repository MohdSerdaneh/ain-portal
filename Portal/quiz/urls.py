from django.urls import path

# Local view imports for quiz operations
from .views import (
    create_question,
    create_question_form,
    delete_question,
    detail_question,
    quizzes,
    update_question,
)

urlpatterns = [
    # Main view to display all quizzes
    path("current-quizzes/", quizzes, name="quizzes"),

    # View for creating a question under a quiz (based on quiz PK)
    path("<pk>/", create_question, name="create_question"),

    # HTMX endpoints for dynamic partial interactions (used in templates)
    path("htmx/question/<pk>/", detail_question, name="detail_question"),
    path("htmx/question/<pk>/update/", update_question, name="update_question"),
    path("htmx/question/<pk>/delete/", delete_question, name="delete_question"),
    path("htmx/create-question-form/", create_question_form, name="create_question_form"),
]
