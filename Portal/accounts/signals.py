from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local imports
from .models import Profile, Student, Teacher

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Automatically create a related profile when a new user is created.

    Depending on the role flags, it creates:
    - Student instance if is_student is True
    - Teacher instance if is_teacher is True
    - General Profile instance otherwise
    """
    if created:
        if instance.is_student:
            print("instance", instance)
            print("email", instance.email)
            Student.objects.create(user=instance, email=instance.email)
        elif instance.is_teacher:
            Teacher.objects.create(user=instance, email=instance.email)
        else:
            Profile.objects.create(user=instance, email=instance.email)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Save the profile after the user instance is saved.
    Ensures that any changes to the user trigger a save on the related profile.
    """
    instance.profile.save()
