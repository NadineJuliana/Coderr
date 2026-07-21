"""
Models for offers and their pricing details.
"""

from django.conf import settings
from django.db import models

# Create your models here.


class Offer(models.Model):
    """
    Stores an offer created by a business user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="offers",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=255,
    )

    image = models.FileField(
        upload_to="offer_images/",
        blank=True,
        null=True,
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        """
        Returns the offer title.
        """

        return self.title


class OfferDetail(models.Model):
    """
    Stores a pricing level belonging to an offer.
    """

    class OfferType(models.TextChoices):
        """
        Defines the available offer detail types.
        """

        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"
        PREMIUM = "premium", "Premium"

    offer = models.ForeignKey(
        Offer,
        related_name="details",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=255,
    )

    revisions = models.PositiveIntegerField()

    delivery_time_in_days = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    features = models.JSONField(
        default=list,
    )

    offer_type = models.CharField(
        max_length=20,
        choices=OfferType.choices,
    )

    def __str__(self):
        """
        Returns the offer title and detail type.
        """

        return f"{self.offer.title} - {self.offer_type}"
