from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

# Local imports
from accounts.models import Teacher
from .models import Course, Report, Report_student, Subject, meetings

User = get_user_model()

# ------------------------------------------------------------------------------------
# 🔹 1. Teacher Profile Forms
# ------------------------------------------------------------------------------------

class UpdateUserForm(forms.ModelForm):
    """Update base user model fields (username & email)."""
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input-i"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"class": "input-i"}),
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class UpdateTeacherProfileForm(forms.ModelForm):
    """Form to update teacher profile information (avatar, full name, age)."""
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            "hidden": "hidden",
            "name": "posti",
            "accept": "image/*",
            "id": "id_posti",
            "class": "img-i-1",
            "onchange": "loadFile(event)",
        })
    )
    age = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input-i"}),
    )
    full_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input-i"}),
    )

    class Meta:
        model = Teacher
        fields = ["avatar", "age", "full_name"]


class FormPasswordChange(PasswordChangeForm):
    """Custom password change form."""
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

# ------------------------------------------------------------------------------------
# 🔹 2. Course & Material Forms
# ------------------------------------------------------------------------------------

class AddCourseForm(forms.ModelForm):
    """Form to create a new course with description and image."""
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Course name",
            "id": "course_name_id"
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            "row": 5,
            "id": "description_id"
        })
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            "hidden": "hidden",
            "name": "posti",
            "accept": "image/*",
            "id": "id_posti",
            "class": "img-i-1",
            "onchange": "loadFile(event)",
        })
    )

    class Meta:
        model = Course
        fields = ["name", "description", "image"]


class AddMaterialForm(forms.ModelForm):
    """Form to upload study material to a course."""
    document = forms.FileField(
        widget=forms.FileInput(attrs={
            "hidden": "hidden",
            "name": "posti",
            "id": "id_posti",
            "class": "img-i-1",
            "onchange": "loadFile()",
        })
    )

    class Meta:
        model = Subject
        fields = ["description", "document"]

# ------------------------------------------------------------------------------------
# 🔹 3. Report & Grade Forms
# ------------------------------------------------------------------------------------

class AddReportForm(forms.ModelForm):
    """Form to create a new report (assignment) with file."""
    document = forms.FileField(
        widget=forms.FileInput(attrs={
            "hidden": "hidden",
            "name": "posti2",
            "id": "id_posti2",
            "class": "img-i-1",
            "onchange": "loadFile2()",
        })
    )

    class Meta:
        model = Report
        fields = ["description_report", "document"]


class UpdateReportGradeForm(forms.ModelForm):
    """Form for teachers to grade and comment on a student's report."""
    class Meta:
        model = Report_student
        fields = ['teacher_notes', 'grade']


class UpdateReportForm(forms.ModelForm):
    """Form to update a report deadline."""
    deadline = forms.DateField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Report
        fields = ['deadline']


# ------------------------------------------------------------------------------------
# 🔹 4. Schedule Meeting Form
# ------------------------------------------------------------------------------------

class schedule_meeting_form(forms.ModelForm):
    """Form to schedule a new meeting for a course."""
    meeting_date = forms.DateField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = meetings
        fields = ['meeting_date']
