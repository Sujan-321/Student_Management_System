from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")

        return email
    
    def clean_username(self):
        username = self.cleaned_data["username"]

        if not re.match(r"^[A-Za-z0-9_]+$", username):
            raise ValidationError(
                "Username can contain only letters, numbers and underscore."
            )

        return username