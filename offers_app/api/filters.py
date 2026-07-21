"""
Filters for narrowing offer list results.
"""

import django_filters

from offers_app.models import Offer


class OfferFilter(django_filters.FilterSet):
    """
    Filters offers by creator, price, and delivery time.
    """

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
        """
        Defines the model and available offer filters.
        """

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
        """
        Filters offers with a minimum price above the given value.
        """

        return queryset.filter(
            min_price__gte=value,
        )

    def filter_max_delivery_time(
        self,
        queryset,
        _,
        value,
    ):
        """
        Filters offers within the given delivery time.
        """

        return queryset.filter(
            min_delivery_time__lte=value,
        )
