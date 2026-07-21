"""
Serializers for creating, retrieving, and updating orders.
"""

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from offers_app.models import OfferDetail
from orders_app.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializes existing orders and validates status updates.
    """

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True,
    )

    class Meta:
        """
        Defines the fields used for existing orders.
        """

        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """
        Validates submitted fields during partial updates.
        """

        if self.partial:
            self.validate_patch_fields()

        return attrs

    def validate_patch_fields(self):
        """
        Ensures that only the order status can be updated.
        """

        allowed_fields = {
            "status",
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
                        "Only the status field "
                        "can be updated."
                    )
                }
            )


class OrderCreateSerializer(
    serializers.ModelSerializer
):
    """
    Creates orders from an existing offer detail.
    """

    offer_detail_id = serializers.IntegerField(
        write_only=True,
    )

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        read_only=True,
    )

    class Meta:
        """
        Defines the fields used when creating orders.
        """

        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
            "offer_detail_id",
        ]

        read_only_fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """
        Creates an order using data from the selected offer detail.
        """

        offer_detail_id = validated_data.pop(
            "offer_detail_id"
        )

        offer_detail = get_object_or_404(
            OfferDetail.objects.select_related(
                "offer__user"
            ),
            id=offer_detail_id,
        )

        return Order.objects.create(
            customer_user=(
                self.context["request"].user
            ),
            business_user=(
                offer_detail.offer.user
            ),
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=(
                offer_detail.delivery_time_in_days
            ),
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
        )
