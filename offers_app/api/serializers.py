"""
Serializers for creating, retrieving, and updating offers.
"""

from django.urls import reverse
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailObjectSerializer(serializers.ModelSerializer):
    """
    Serializes complete offer detail objects.
    """

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
    )

    class Meta:
        """
        Defines the fields used for offer details.
        """

        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]
        read_only_fields = [
            "id",
        ]


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """
    Serializes offer detail identifiers and URLs.
    """

    url = serializers.SerializerMethodField()

    class Meta:
        """
        Defines the fields used for offer detail links.
        """

        model = OfferDetail
        fields = [
            "id",
            "url",
        ]

    def get_url(self, obj):
        """
        Returns the relative or absolute offer detail URL.
        """

        path = reverse(
            "offer-detail-object",
            kwargs={"pk": obj.pk},
        )

        request = self.context.get("request")

        if request is None:
            return path

        return request.build_absolute_uri(path)


class OfferBaseSerializer(serializers.ModelSerializer):
    """
    Provides shared fields for offer serializers.
    """

    min_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
        coerce_to_string=False,
    )

    min_delivery_time = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        """
        Defines the shared offer fields.
        """

        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "min_price",
            "min_delivery_time",
        ]


class OfferUserDetailsSerializer(serializers.Serializer):
    """
    Serializes basic information about an offer creator.
    """

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(OfferBaseSerializer):
    """
    Serializes offers for list responses.
    """

    details = OfferDetailLinkSerializer(
        many=True,
        read_only=True,
    )

    user_details = OfferUserDetailsSerializer(
        source="user",
        read_only=True,
    )

    class Meta(OfferBaseSerializer.Meta):
        """
        Adds creator details to the shared offer fields.
        """

        fields = OfferBaseSerializer.Meta.fields + [
            "user_details",
        ]


class OfferRetrieveSerializer(OfferBaseSerializer):
    """
    Serializes a single offer with detail links.
    """

    details = OfferDetailLinkSerializer(
        many=True,
        read_only=True,
    )


class OfferWriteSerializer(serializers.ModelSerializer):
    """
    Serializes and validates offer creation and updates.
    """

    details = OfferDetailObjectSerializer(
        many=True,
    )

    class Meta:
        """
        Defines writable offer fields.
        """

        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]
        read_only_fields = [
            "id",
        ]

    def validate_details(self, value):
        """
        Validates offer details for creation or updates.
        """

        if self.instance is None:
            self.validate_create_details(value)
        else:
            self.validate_update_details(value)

        return value

    def validate_create_details(self, details):
        """
        Ensures that new offers contain exactly three details.
        """

        if len(details) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly three details."
            )

        self.validate_unique_offer_types(details)

    def validate_update_details(self, details):
        """
        Ensures that updated details include an offer type.
        """

        for detail in details:
            if not detail.get("offer_type"):
                raise serializers.ValidationError(
                    "Each detail must include an offer_type."
                )

        self.validate_unique_offer_types(details)

    def validate_unique_offer_types(self, details):
        """
        Ensures that every offer type occurs only once.
        """

        offer_types = [
            detail.get("offer_type")
            for detail in details
        ]

        if len(offer_types) != len(set(offer_types)):
            raise serializers.ValidationError(
                "Each offer_type may only occur once."
            )

    def create(self, validated_data):
        """
        Creates an offer and its related details.
        """

        details_data = validated_data.pop("details")

        offer = Offer.objects.create(
            **validated_data,
        )

        self.create_offer_details(
            offer,
            details_data,
        )

        return offer

    def create_offer_details(
        self,
        offer,
        details_data,
    ):
        """
        Creates all details belonging to an offer.
        """

        for detail_data in details_data:
            OfferDetail.objects.create(
                offer=offer,
                **detail_data,
            )

    def update(self, instance, validated_data):
        """
        Updates an offer and its submitted details.
        """

        details_data = validated_data.pop(
            "details",
            [],
        )

        instance = super().update(
            instance,
            validated_data,
        )

        self.update_offer_details(
            instance,
            details_data,
        )

        return instance

    def update_offer_details(
        self,
        offer,
        details_data,
    ):
        """
        Updates each submitted offer detail.
        """

        for detail_data in details_data:
            self.update_offer_detail(
                offer,
                detail_data,
            )

    def update_offer_detail(
        self,
        offer,
        detail_data,
    ):
        """
        Updates the matching detail for an offer type.
        """

        offer_type = detail_data.get("offer_type")

        try:
            detail = offer.details.get(
                offer_type=offer_type,
            )
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "details": (
                        "No matching detail exists "
                        f"for offer_type '{offer_type}'."
                    )
                }
            )

        for field, value in detail_data.items():
            setattr(
                detail,
                field,
                value,
            )

        detail.save()
