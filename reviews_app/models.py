"""
Review model for customer ratings of business users.
"""

from django.db import models
from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)

# Create your models here.


class Review(models.Model):
    """
    Stores a customer review for a business user.
    """

    business_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews",
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="written_reviews",
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        """
        Defines database constraints for reviews.
        """

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "business_user",
                    "reviewer",
                ],
                name=(
                    "unique_review_per_business_user"
                ),
            ),
        ]

    def __str__(self):
        """
        Returns the reviewer, business user, and rating.
        """

        return (
            f"{self.reviewer} - "
            f"{self.business_user}: "
            f"{self.rating}"
        )
