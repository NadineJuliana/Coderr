"""
Profile model for storing additional user information.
"""

from django.conf import settings
from django.db import models

# Create your models here.


class Profile(models.Model):
    """
    Stores additional information associated with a user account.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    file = models.FileField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )
    tel = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )
    description = models.TextField(
        blank=True,
        default="",
    )
    working_hours = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        """
        Returns the username associated with the profile.
        """

        return f"Profile of {self.user.username}"
