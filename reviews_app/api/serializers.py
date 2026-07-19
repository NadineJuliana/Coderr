from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from reviews_app.models import Review


User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
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
        if self.partial:
            self.validate_patch_fields()

        return attrs

    def validate_patch_fields(self):
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
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(
            type="business",
        ),
    )

    class Meta:
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
        return Review.objects.create(
            reviewer=self.context["request"].user,
            **validated_data,
        )
