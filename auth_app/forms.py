from django.contrib.auth.forms import (
    AdminUserCreationForm,
    UserChangeForm,
)

from auth_app.models import User


class CustomUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )
