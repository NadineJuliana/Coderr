"""
Serializers for creating, retrieving, and updating reviews.
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from reviews_app.models import Review


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializes existing reviews and validates review updates.
    """

    class Meta:
        """
        Defines the fields used for existing reviews.
        """

        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "business_user",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """
        Validates submitted fields during partial review updates.
        """

        if self.partial:
            self.validate_patch_fields()

        return attrs

    def validate_patch_fields(self):
        """
        Ensures that only rating and description can be updated.
        """

        allowed_fields = {
            "rating",
            "description",
        }

        submitted_fields = set(
            self.initial_data.keys()
        )

        invalid_fields = (
            submitted_fields - allowed_fields
        )

        if invalid_fields:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "Only rating and description "
                        "can be updated."
                    )
                }
            )


class ReviewCreateSerializer(
    serializers.ModelSerializer
):
    """
    Serializes and validates newly created reviews.
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(
            type="business",
        ),
    )

    class Meta:
        """
        Defines the fields used when creating reviews.
        """

        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "reviewer",
            "created_at",
            "updated_at",
        ]

    def validate_business_user(
        self,
        business_user,
    ):
        """
        Prevents duplicate reviews for the same business user.
        """

        reviewer = self.context["request"].user

        review_exists = Review.objects.filter(
            business_user=business_user,
            reviewer=reviewer,
        ).exists()

        if review_exists:
            raise PermissionDenied(
                "You have already reviewed "
                "this business user."
            )

        return business_user

    def create(self, validated_data):
        """
        Creates a review using the authenticated user as reviewer.
        """

        return Review.objects.create(
            reviewer=self.context["request"].user,
            **validated_data,
        )
