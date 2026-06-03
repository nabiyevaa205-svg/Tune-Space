from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or email",
        widget=forms.TextInput(attrs={"placeholder": "Enter username or email", "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password", "autocomplete": "current-password"}),
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


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        label="First name",
        widget=forms.TextInput(attrs={"placeholder": "First name"}),
    )
    last_name = forms.CharField(
        required=False,
        label="Last name",
        widget=forms.TextInput(attrs={"placeholder": "Last name"}),
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "example@mail.com"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        exists = User.objects.exclude(pk=self.instance.pk).filter(username__iexact=username).exists()
        if exists:
            raise forms.ValidationError("This username is already taken.")
        return username


class UserProfileForm(forms.ModelForm):
    INTEREST_CHOICES = [
        ("pop", "Pop"),
        ("kpop", "K-pop"),
        ("rnb", "R&B"),
        ("rock", "Rock"),
        ("jazz", "Jazz"),
        ("live", "Live shows"),
        ("playlists", "Playlists"),
        ("dance", "Dance"),
    ]

    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = UserProfile
        fields = ("display_name", "photo", "age", "gender", "city", "interests", "subscription")
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "Display name"}),
            "age": forms.NumberInput(attrs={"placeholder": "Age", "min": "1"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "subscription": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.interests:
            self.initial["interests"] = [item for item in self.instance.interests.split(",") if item]

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.interests = ",".join(self.cleaned_data.get("interests", []))
        if commit:
            profile.save()
        return profile


class NotificationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("email_notifications", "release_notifications")
