from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render

from books.models import Book

from .forms import NotificationForm, ProfileForm, RegisterForm, UserProfileForm
from .models import UserProfile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("account")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def account(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    favorite_tracks = Book.objects.select_related("author").order_by("-created_at")[:6]
    playable_count = sum(1 for track in favorite_tracks if track.audio_file)
    return render(
        request,
        "users/account.html",
        {
            "favorite_tracks": favorite_tracks,
            "playable_count": playable_count,
            "profile": profile,
        },
    )


@login_required
def profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    active_section = request.POST.get("section", "profile") if request.method == "POST" else "profile"
    if request.method == "POST":
        account_form = ProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        password_form = PasswordChangeForm(request.user, request.POST)
        notification_form = NotificationForm(request.POST, instance=user_profile)

        if active_section == "profile" and account_form.is_valid() and profile_form.is_valid():
            account_form.save()
            profile_form.save()
            return redirect("account")
        if active_section == "password" and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect("profile")
        if active_section == "notifications" and notification_form.is_valid():
            notification_form.save()
            return redirect("profile")
        if active_section == "verification":
            user_profile.verification_requested = True
            user_profile.save(update_fields=["verification_requested"])
            return redirect("profile")
    else:
        account_form = ProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
        password_form = PasswordChangeForm(request.user)
        notification_form = NotificationForm(instance=user_profile)

    return render(
        request,
        "users/profile.html",
        {
            "account_form": account_form,
            "profile_form": profile_form,
            "password_form": password_form,
            "notification_form": notification_form,
            "profile": user_profile,
            "active_section": active_section,
        },
    )
