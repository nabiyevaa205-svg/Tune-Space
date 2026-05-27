from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or email",
        widget=forms.TextInput(
            attrs={"placeholder": "Enter username or email", "autocomplete": "username"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter password", "autocomplete": "current-password"}
        ),
    )

    error_messages = {
        "invalid_login": "Invalid username/email or password.",
        "inactive": "This account is inactive.",
    }

    def clean_username(self):
        value = self.cleaned_data.get("username", "").strip()
        if "@" in value:
            user = User.objects.filter(email__iexact=value).first()
            if user:
                return user.username
        return value


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Choose a username"}),
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "example@mail.com"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Create a strong password"}),
        help_text="",
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat password"}),
        help_text="",
    )

    error_messages = {
        "password_mismatch": "Passwords do not match.",
    }

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
