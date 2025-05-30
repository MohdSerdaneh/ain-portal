from django import forms

from src.current_user import get_current_user
from accounts.models import Teacher
from teacher.models import Course
from .models import QuestionAnswer, Quiz

# ================================
# Form: Create Quiz
# ================================
class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("id", "course", "name", "number_of_questions", "time")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        teacher = Teacher.objects.get(user=get_current_user())
        course = Course.objects.filter(teacher=teacher)
        self.fields["course"].queryset = course

# ================================
# Form: Create QuestionAnswer
# ================================
class CreateQuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = (
            "id",
            "question",
            "option1",
            "option2",
            "option3",
            "option4",
            "correct",
        )
