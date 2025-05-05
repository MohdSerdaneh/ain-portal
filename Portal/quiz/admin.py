from django.contrib import admin

# Local imports
from .models import QuestionAnswer, Quiz, QuizStudent

# Inline model to allow QuestionAnswer to be added within the Quiz admin page
class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer
    extra = 1  # Optional: Show 1 empty row for new question creation by default

# Customize the admin view for Quiz
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionAnswerInline]  # Display related questions inline with each quiz

# Customize the admin view for individual questions
@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "id")  # Show question and ID in the admin table

# Customize admin view for students who took quizzes
@admin.register(QuizStudent)
class QuizStudentAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz")  # Show student attempt ID and associated quiz
