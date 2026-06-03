from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("account/", views.account, name="account"),
    path("profile/", views.profile, name="profile"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]
