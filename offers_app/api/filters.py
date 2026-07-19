import django_filters

from offers_app.models import Offer


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(
        field_name="user_id",
    )

    min_price = django_filters.NumberFilter(
        method="filter_min_price",
    )

    max_delivery_time = django_filters.NumberFilter(
        method="filter_max_delivery_time",
    )

    class Meta:
        model = Offer
        fields = [
            "creator_id",
            "min_price",
            "max_delivery_time",
        ]

    def filter_min_price(
        self,
        queryset,
        _,
        value,
    ):
        return queryset.filter(
            min_price__gte=value,
        )

    def filter_max_delivery_time(
        self,
        queryset,
        _,
        value,
    ):
        return queryset.filter(
            min_delivery_time__lte=value,
        )
