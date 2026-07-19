from django.contrib import admin
from orders_app.models import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "customer_user",
        "business_user",
        "offer_type",
        "status",
        "price",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "status",
        "offer_type",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "customer_user__username",
        "customer_user__email",
        "business_user__username",
        "business_user__email",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-created_at",
    ]
