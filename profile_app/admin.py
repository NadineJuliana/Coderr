from django.contrib import admin
from profile_app.models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "get_username",
        "get_email",
        "get_type",
        "location",
        "created_at",
    ]

    list_filter = [
        "user__type",
        "created_at",
    ]

    search_fields = [
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
        "location",
        "tel",
    ]

    readonly_fields = [
        "created_at",
    ]

    fieldsets = [
        (
            "User",
            {
                "fields": [
                    "user",
                ],
            },
        ),
        (
            "Profile information",
            {
                "fields": [
                    "file",
                    "location",
                    "tel",
                    "description",
                    "working_hours",
                ],
            },
        ),
        (
            "Metadata",
            {
                "fields": [
                    "created_at",
                ],
            },
        ),
    ]

    @admin.display(
        description="Username",
        ordering="user__username",
    )
    def get_username(self, obj):
        return obj.user.username

    @admin.display(
        description="Email",
        ordering="user__email",
    )
    def get_email(self, obj):
        return obj.user.email

    @admin.display(
        description="Type",
        ordering="user__type",
    )
    def get_type(self, obj):
        return obj.user.type
