"""
Custom user model for the application.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
    Extends Django's default user model with a user type.
    """

    class UserType(models.TextChoices):
        """
        Defines the available user types.
        """

        CUSTOMER = "customer", "Customer"
        BUSINESS = "business", "Business"

    type = models.CharField(
        max_length=20,
        choices=UserType.choices,
    )

    def __str__(self):
        """
        Returns the username as the string representation.
        """

        return self.username
