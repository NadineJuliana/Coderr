"""
Filters for narrowing review list results.
"""

from django_filters import rest_framework as filters

from reviews_app.models import Review


class ReviewFilter(filters.FilterSet):
    """
    Filters reviews by business user or reviewer.
    """

    business_user_id = filters.NumberFilter(
        field_name="business_user_id",
    )

    reviewer_id = filters.NumberFilter(
        field_name="reviewer_id",
    )

    class Meta:
        """
        Defines the model and available review filters.
        """

        model = Review
        fields = [
            "business_user_id",
            "reviewer_id",
        ]
