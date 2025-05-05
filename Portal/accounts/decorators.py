from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

# App imports
from accounts.models import Student
from quiz.models import Quiz, QuizStudent
from teacher.models import Course

User = get_user_model()

# --------------------------------------------------
# Decorators for Access Control & Routing
# --------------------------------------------------

def unAuth_user(view_fun):
    """
    Redirects authenticated users away from login/register pages.
    """
    def wrapper_fun(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return view_fun(request, *args, **kwargs)
    return wrapper_fun


def allow_user(user_permission_list):
    """
    Allows access to the view for users with specific roles.
    Logs out and redirects otherwise.
    """
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            try:
                if request.user.is_teacher or request.user.is_student or request.user.is_admin:
                    return view_func(request, *args, **kwargs)
                else:
                    logout(request)
                    return redirect("/")
            except:
                logout(request)
                return redirect("/")
        return inner
    return decorator


def allow_courses_student():
    """
    Ensures the student has access to the course by checking their enrollment.
    Raises 404 if unauthorized.
    """
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            course = get_object_or_404(Course, name=kwargs.get("name"))
            student = Student.objects.get(user=request.user)
            enrolled_courses = Course.objects.filter(student=student)

            if course in enrolled_courses:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404()
        return inner
    return decorator


def allow_quiz_student():
    """
    Ensures the student is attempting their own quiz.
    Raises 404 or returns message if unauthorized.
    """
    def decorator(view_func):
        def inner(request, *args, **kwargs):
            try:
                quiz = get_object_or_404(QuizStudent, pk=kwargs.get("pk"))
                student = Student.objects.get(user=request.user)
                student_quizzes = QuizStudent.objects.filter(student=student)
            except quiz.DoesNotExist:
                return HttpResponse("No Quizzes yet!")

            if quiz in student_quizzes:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404()
        return inner
    return decorator
