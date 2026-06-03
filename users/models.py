from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ("", "Not set"),
        ("female", "Female"),
        ("male", "Male"),
        ("other", "Other"),
    ]
    SUBSCRIPTION_CHOICES = [
        ("free", "Free"),
        ("premium", "Premium"),
        ("gold", "Gold"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    city = models.CharField(max_length=120, blank=True)
    interests = models.TextField(blank=True)
    subscription = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default="free")
    email_notifications = models.BooleanField(default=True)
    release_notifications = models.BooleanField(default=True)
    verification_requested = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name or self.user.username
