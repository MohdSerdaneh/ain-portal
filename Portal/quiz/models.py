from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.models import Student
# Local imports goes here
from teacher.models import Course, Teacher
# ================================
# Model: Quiz
# ================================

class Quiz(models.Model):
    author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    number_of_questions = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, through="QuizStudent")

    def __str__(self):
        return self.name
# ================================
# Model: QuizStudent (Enrollment)
# ================================

class QuizStudent(models.Model):
    """
       Intermediate model linking a Student to a Quiz.
       Tracks progress, score, and status.
       """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)
    score = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    # take_it = models.BooleanField(default=False)
    class Meta:
        unique_together = [["student", "quiz"]] # Prevents duplicate entries

    def __str__(self):
        return self.quiz.name

    # @property
    # def has_take(self) -> bool:
    #     return self.take_it

# ================================
# Model: QuestionAnswer
# ================================
class QuestionAnswer(models.Model):
    """
       Stores MCQ-type questions for each quiz.
       """
    CHOICES = (
        ("a", "a"),
        ("b", "b"),
        ("c", "c"),
        ("d", "d"),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct = models.CharField(max_length=200, choices=CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        unique_together = [
            ["question", "quiz", "option1", "option2", "option3", "option4"]
        ]
        verbose_name = _("Question Answer")
