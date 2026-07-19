from django.urls import reverse
from rest_framework import serializers

from offers_app.models import Offer, OfferDetail


class OfferDetailObjectSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
    )

    class Meta:
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
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "url",
        ]

    def get_url(self, obj):
        path = reverse(
            "offer-detail-object",
            kwargs={"pk": obj.pk},
        )

        request = self.context.get("request")

        if request is None:
            return path

        return request.build_absolute_uri(path)


class OfferBaseSerializer(serializers.ModelSerializer):
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


class OfferUserDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(OfferBaseSerializer):
    details = OfferDetailLinkSerializer(
        many=True,
        read_only=True,
    )

    user_details = OfferUserDetailsSerializer(
        source="user",
        read_only=True,
    )

    class Meta(OfferBaseSerializer.Meta):
        fields = OfferBaseSerializer.Meta.fields + [
            "user_details",
        ]


class OfferRetrieveSerializer(OfferBaseSerializer):
    details = OfferDetailLinkSerializer(
        many=True,
        read_only=True,
    )


class OfferWriteSerializer(serializers.ModelSerializer):
    details = OfferDetailObjectSerializer(
        many=True,
    )

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "details",
        ]
        read_only_fields = [
            "id",
            "user",
        ]

    def validate_details(self, value):
        if self.instance is None and len(value) != 3:
            raise serializers.ValidationError(
                "An offer must contain exactly three details."
            )

        return value

    def create(self, validated_data):
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
        for detail_data in details_data:
            OfferDetail.objects.create(
                offer=offer,
                **detail_data,
            )

    def update(self, instance, validated_data):
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
        offer_type = detail_data.get("offer_type")

        detail = offer.details.get(
            offer_type=offer_type,
        )

        for field, value in detail_data.items():
            setattr(
                detail,
                field,
                value,
            )

        detail.save()
