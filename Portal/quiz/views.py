from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

# Local imports
from accounts.models import Profile, Student
from teacher.models import Course, Teacher
from .forms import CreateQuestionAnswerForm, CreateQuizForm
from .models import QuestionAnswer, Quiz, QuizStudent


# ================================
# View: Display and Create Quizzes
# ================================
@login_required(login_url="login_view")
def quizzes(request):
    author = Teacher.objects.get(user=request.user)
    quizzes = Quiz.objects.filter(author=author)
    user_profile = Profile.objects.get(user=request.user)
    msg = ""

    if request.method == "POST":
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.author = author
            course = temp.course
            try:
                students = Course.objects.filter(name=course).values("student")
                if students[0]["student"] is not None:
                    temp.save()
                else:
                    msg = "No enrolled students currently in the course"
                    return render(request, "quiz/quiz_list.html", {
                        "form": form,
                        "msg": msg
                    })

                for i in students:
                    student = Student.objects.get(id=i["student"])
                    quiz_instance = Quiz.objects.get(name=temp.name)
                    QuizStudent.objects.create(
                        student=student,
                        course=course,
                        quiz=quiz_instance
                    )
            except:
                msg = "ERROR"
                return render(request, "quiz/quiz_list.html", {
                    "form": form,
                    "msg": msg
                })
        else:
            msg = "Form is not valid"
        return redirect("quizzes")

    else:
        form = CreateQuizForm()

    return render(request, "quiz/quiz_list.html", {
        "quizzes": quizzes,
        "user_profile": user_profile,
        "form": form,
        "msg": msg,
    })


# ================================
# View: Create Question for a Quiz
# ================================
@login_required(login_url="login_view")
def create_question(request, pk):
    quiz = Quiz.objects.get(id=pk)
    questions = QuestionAnswer.objects.filter(quiz=quiz)
    form = CreateQuestionAnswerForm(request.POST or None)
    msg = None
    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        if form.is_valid():
            try:
                question = form.save(commit=False)
                question.quiz = quiz
                question.save()
                return redirect("detail_question", pk=question.id)
            except:
                msg = "Question already exists!"

        return render(
            request,
            "quiz/partials/create_question_answer_form.html",
            context={"form": form, "msg": msg}
        )

    context = {
        "form": form,
        "questions": questions,
        "quiz": quiz,
        "user_profile": user_profile,
    }
    return render(request, "quiz/create_question_answer.html", context)


# ================================
# View: Load Create Question Form (HTMX Partial)
# ================================
@login_required(login_url="login_view")
def create_question_form(request):
    form = CreateQuestionAnswerForm()
    return render(request, "quiz/partials/create_question_answer_form.html", {"form": form})


# ================================
# View: Delete Question (HTMX/AJAX)
# ================================
def delete_question(request, pk):
    question = get_object_or_404(QuestionAnswer, id=pk)
    if request.method == "POST":
        question.delete()
        return HttpResponse("")
    return HttpResponseNotAllowed(["POST"])


# ================================
# View: Detail of a Question (HTMX Partial)
# ================================
@login_required(login_url="login_view")
def detail_question(request, pk):
    question = get_object_or_404(QuestionAnswer, id=pk)
    return render(request, "quiz/partials/quiz_detail.html", {"question": question})


# ================================
# View: Update an Existing Question (HTMX)
# ================================
@login_required(login_url="login_view")
def update_question(request, pk):
    question = get_object_or_404(QuestionAnswer, id=pk)
    form = CreateQuestionAnswerForm(request.POST or None, instance=question)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("detail_question", pk=question.id)

    return render(request, "quiz/partials/create_question_answer_form.html", {
        "question": question,
        "form": form,
    })
