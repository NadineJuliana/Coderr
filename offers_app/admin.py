from django.contrib import admin
from offers_app.models import Offer, OfferDetail

# Register your models here.


class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 0


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "user",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "description",
        "user__username",
        "user__email",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    inlines = [
        OfferDetailInline,
    ]


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "offer",
        "offer_type",
        "price",
        "delivery_time_in_days",
    ]

    list_filter = [
        "offer_type",
        "delivery_time_in_days",
    ]

    search_fields = [
        "title",
        "offer__title",
        "offer__user__username",
    ]
