"""
Serializers for profile detail and profile list endpoints.
"""

from rest_framework import serializers

from profile_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializes detailed profile data and supports profile updates.
    """

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )
    first_name = serializers.CharField(
        source="user.first_name",
        required=False,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        source="user.last_name",
        required=False,
        allow_blank=True,
    )
    type = serializers.CharField(
        source="user.type",
        read_only=True,
    )
    email = serializers.EmailField(
        source="user.email",
        required=False,
    )

    class Meta:
        """
        Defines the profile fields used by the serializer.
        """

        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]
        read_only_fields = [
            "user",
            "created_at",
        ]

    def update(self, instance, validated_data):
        """
        Updates profile data and related user information.
        """

        user_data = validated_data.pop("user", {})

        user = instance.user
        user.first_name = user_data.get(
            "first_name",
            user.first_name,
        )
        user.last_name = user_data.get(
            "last_name",
            user.last_name,
        )
        user.email = user_data.get(
            "email",
            user.email,
        )
        user.save()

        return super().update(
            instance,
            validated_data,
        )


class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializes profile data for business profile lists.
    """

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )
    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )
    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )
    type = serializers.CharField(
        source="user.type",
        read_only=True,
    )

    class Meta:
        """
        Defines the fields returned for business profiles.
        """

        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializes profile data for customer profile lists.
    """

    username = serializers.CharField(
        source="user.username",
        read_only=True,
    )
    first_name = serializers.CharField(
        source="user.first_name",
        read_only=True,
    )
    last_name = serializers.CharField(
        source="user.last_name",
        read_only=True,
    )
    type = serializers.CharField(
        source="user.type",
        read_only=True,
    )

    class Meta:
        """
        Defines the fields returned for customer profiles.
        """

        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "type",
        ]
