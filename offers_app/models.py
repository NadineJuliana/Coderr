from django.conf import settings
from django.db import models

# Create your models here.


class Offer(models.Model):
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
        return self.title


class OfferDetail(models.Model):

    class OfferType(models.TextChoices):
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
        return f"{self.offer.title} - {self.offer_type}"
