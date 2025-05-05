from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

# Local model imports
from .models import Contact, User

# Use the custom User model
User = get_user_model()


class LoginForm(forms.Form):
    """
    Basic login form with username and password input fields.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "id": "username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "  Password", "id": "password1"}
        )
    )


class SignUpForm(UserCreationForm):
    """
    Registration form for new users with custom fields from the custom User model.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "id": "password1"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "id": "password2"}
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
        # error_messages can be added here if needed
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "is_student",
            "is_teacher",
            "is_admin",
        )


class ContactForm(forms.ModelForm):
    """
    Contact form linked to the Contact model, for user messages or feedback.
    """
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"id": "name", "type": "name", "name": "name", "placeholder": "Name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "id": "email",
                "type": "email",
                "name": "email",
                "placeholder": "Email",
            }
        ),
    )
    desc = forms.CharField(
        widget=forms.Textarea(
            attrs={"id": "desc", "name": "desc", "placeholder": "Message Description"}
        ),
    )

    class Meta:
        model = Contact
        fields = ("name", "email", "desc")
