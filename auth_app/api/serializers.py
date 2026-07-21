"""
Serializers for user registration and login.
"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from profile_app.models import Profile

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    """
    Validates registration data and creates a new user account.
    """

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=User.UserType.choices,
    )

    def validate(self, attrs):
        """
        Checks whether both submitted passwords match.
        """

        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({
                "repeated_password": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        """
        Creates a new user together with an empty profile.
        """

        validated_data.pop("repeated_password")

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data["type"],
        )

        Profile.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    """
    Authenticates a user using the provided credentials.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Verifies the username and password combination.
        """

        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )

        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password."
            )

        attrs["user"] = user

        return attrs
