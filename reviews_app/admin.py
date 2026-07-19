from django.contrib import admin
from reviews_app.models import Review

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "business_user",
        "reviewer",
        "rating",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "rating",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "business_user__username",
        "business_user__email",
        "reviewer__username",
        "reviewer__email",
        "description",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-updated_at",
    ]
