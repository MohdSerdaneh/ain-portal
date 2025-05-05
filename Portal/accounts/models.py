from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

# Local utility imports for avatar storage paths
from .utils import student_directory_path, teacher_directory_path


class User(AbstractUser):
    """
    Extends Django's built-in User model to include role flags.
    """
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    class Meta:
        app_label = 'accounts'  # ✅ Explicitly declare app ownership


class Contact(models.Model):
    """
    Stores contact form submissions from users.
    """
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=120)
    desc = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'accounts'  # ✅


class Profile(models.Model):
    """
    Abstract profile base class extended by Student and Teacher.
    Stores shared fields like name, interest, and email.
    """
    INTEREST_CHOICES = (
        ("programming", "Programming"),
        ("testing", "Testing"),
        ("control", "Control"),
    )
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True
    )
    age = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=122, null=True, blank=True)
    intersted_with = models.CharField(
        max_length=11, default="programming", choices=INTEREST_CHOICES
    )
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'accounts'  # ✅


class Student(Profile):
    """
    Extends Profile for student-specific features (e.g., avatar).
    Resizes avatar image if too large.
    """
    avatar = models.ImageField(default="default.png", upload_to=student_directory_path)

    class Meta:
        verbose_name = "Student Profile"
        app_label = 'accounts'  # ✅

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)


class Teacher(Profile):
    """
    Extends Profile for teacher-specific features (e.g., avatar).
    Resizes avatar image if too large.
    """
    avatar = models.ImageField(default="default.png", upload_to=teacher_directory_path)

    class Meta:
        verbose_name = "Teacher Profile"
        app_label = 'accounts'  # ✅

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
