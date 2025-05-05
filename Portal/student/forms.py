from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

# Local imports
from accounts.models import Student
from teacher.models import Report_student

User = get_user_model()

# -------------------------------------
# Form: Update User's Basic Info (username/email)
# -------------------------------------
class UpdateUserForm(forms.ModelForm):
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


# -------------------------------------
# Form: Update Student Profile (avatar, age, name)
# -------------------------------------
class UpdateStudentProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={
            "hidden": "hidden",
            "name": "posti",
            "accept": "image/*",
            "id": "id_posti",
            "class": "img-i-1",
            "onchange": "loadFile(event)",  # JS preview handler
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
        model = Student
        fields = ["avatar", "age", "full_name"]


# -------------------------------------
# Form: Change Password (extends built-in)
# -------------------------------------
class FormPasswordChange(PasswordChangeForm):
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


# -------------------------------------
# Form: Update Academic Report (Teacher-to-Student)
# -------------------------------------
class UpdateReportForm(forms.ModelForm):
    class Meta:
        model = Report_student
        fields = ["student_notes", "report_file"]
