from django.urls import path
from . import views
from .views import course_detail, upload_report_file, dismiss_request

urlpatterns = [
    # Student Dashboard
    path("dashboard/", views.student_dashboard, name="student_dashboard"),

    # Join Course via Course Name (slug-style)
    path("dashboard/join_course/<str:name>/", views.join_course, name="join_course"),

    # Search for Courses
    path("dashboard/search/", views.search, name="search"),

    # Profile Information and Management
    path("profile-info", views.profile_student_view, name="profile_student_view"),
    path("update-profile", views.update_student_profile, name="update_student_profile"),
    path("reset-password", views.reset_password_view, name="reset_password_view"),

    # Course Overview
    path("courses/", views.courses, name="student_courses"),
    path("course-detail/<str:name>/", course_detail, name="course_detail"),

    # File Upload for Reports
    path("upload-report-file/<int:id>/", upload_report_file, name="upload_report_file"),
    path('upload-report/<int:report_id>/', views.upload_report_file, name='upload_report_file'),

    # Quiz View
    path("current-quizzes", views.current_quizzes, name="current_quizzes"),

    # View & Dismiss Join Requests
    path("student-reqeusts", views.student_reqeusts, name="student_reqeusts"),
    path("dismiss/<str:name>/<str:std_name>/", dismiss_request, name="dismiss_request"),

    # Start Quiz
    path("start-quiz/<int:pk>/", views.start_quiz, name="start_quiz"),

]
