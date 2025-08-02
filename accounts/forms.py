from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with the given email already exists."
            )
        return email
