from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    PLAN_CHOICES = [
        ('none', 'No Plan'),
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]

    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='none')
    free_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
