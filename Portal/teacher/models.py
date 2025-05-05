from django.db import models
from django.urls import reverse
from django.utils import timezone

# Account relations
from accounts.models import Student, Teacher

# Utility paths for storing uploaded media
from .utils import (
    course_directory_path,
    report_directory_path,
    students_report_directory_path,
    subject_directory_path,
)

# -------------------------------------------------------------------------
# Course Model
# -------------------------------------------------------------------------
class Course(models.Model):
    student = models.ManyToManyField(
        Student, null=True, blank=True, related_name="student"
    )
    name = models.CharField(max_length=60, null=True, blank=True, unique=True)
    description = models.TextField(max_length=200, null=True, blank=True, default="")
    image = models.ImageField(
        default="course_images/default.png",
        upload_to=course_directory_path,
        null=True,
        blank=True,
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    # URL helper methods
    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"name": self.name})

    def get_add_student_url(self):
        return reverse("add_student", kwargs={"name": self.name})

    def get_add_material_url(self):
        return reverse("add_material", kwargs={"name": self.name})

    def get_add_report_url(self):
        return reverse("add_report", kwargs={"name": self.name})

    def create_meeting_url(self):
        return reverse("join_meeting", kwargs={"name": self.name})

# -------------------------------------------------------------------------
# Optional Enrollment Table (if you want to track join dates separately)
# -------------------------------------------------------------------------
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["student", "course"]]

    def __str__(self):
        return str(self.student)

# -------------------------------------------------------------------------
# Subject / Material Upload
# -------------------------------------------------------------------------
class Subject(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.CharField(max_length=400, null=True, blank=True, default="")
    document = models.FileField(upload_to=subject_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("subjects:subject_detail", kwargs={"slug": self.slug})

    def get_courses_related_to_memberships(self):
        return self.courses.all()  # Not typically used unless M2M to courses

# -------------------------------------------------------------------------
# Reports Model (Assigned by Teacher to a Course)
# -------------------------------------------------------------------------
class Report(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description_report = models.CharField(max_length=400, null=True, blank=True, default="")
    document = models.FileField(upload_to=report_directory_path)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, through="Report_student")  # Many-to-many via intermediate model
    deadline = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description_report

    def get_absolute_url(self):
        return reverse("reports:report_detail", kwargs={"slug": self.slug})

    def get_courses_related_to_memberships(self):
        return self.courses.all()

# -------------------------------------------------------------------------
# Report Submission and Grading per Student
# -------------------------------------------------------------------------
class Report_student(models.Model):
    CHOICES = (
        ("Not Submitted", "Not Submitted"),
        ("Not Graded", "Not Graded"),
        ("Satisfactory", "Satisfactory"),
        ("Good", "Good"),
        ("Merit", "Merit"),
        ("Excellent", "Excellent"),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to=students_report_directory_path, blank=True, null=True)
    grade = models.CharField(max_length=200, choices=CHOICES, default="Not Submitted")
    teacher_notes = models.TextField(blank=True, null=True)
    student_notes = models.TextField(blank=True, null=True)
    done = models.BooleanField(default=False)
    last_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [["student", "report"]]  # Ensures a student submits once per report

    def __str__(self):
        return f"{self.student} : {self.report}"

# -------------------------------------------------------------------------
# Meeting Model for Scheduling Live/ASL Sessions
# -------------------------------------------------------------------------
class meetings(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description_meeting = models.CharField(max_length=400, null=True, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    meeting_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description_meeting

# -------------------------------------------------------------------------
# Join Request System (Student Requests to Join Courses)
# -------------------------------------------------------------------------
class JoinCourseList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.course} - {self.student}"
