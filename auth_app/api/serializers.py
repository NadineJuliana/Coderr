from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(
        choices=User.UserType.choices,
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError({
                "repeated_password": "Passwords do not match."
            })

        return attrs

    def create(self, validated_data):
        validated_data.pop("repeated_password")

        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data["type"],
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
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
