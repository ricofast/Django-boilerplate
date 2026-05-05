from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class UserRegistrationForm(SignupForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        user.save(update_fields=["first_name", "last_name"])
        return user


class UserLoginForm(LoginForm):
    """Extension hook for future login customization beyond allauth defaults."""


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio", "avatar_url"]
