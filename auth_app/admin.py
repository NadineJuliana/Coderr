from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from auth_app.forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
)

from auth_app.models import User

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = (
        "username",
        "email",
        "is_staff",
        "is_active",
    )


admin.site.register(User, CustomUserAdmin)
