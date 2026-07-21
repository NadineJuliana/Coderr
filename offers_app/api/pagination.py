"""
Pagination settings and validation for offer lists.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


class OfferPagination(PageNumberPagination):
    """
    Paginates offer lists and validates custom page sizes.
    """

    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_page_size(self, request):
        """
        Returns and validates the requested page size.
        """

        page_size = request.query_params.get(self.page_size_query_param)

        if page_size is None:
            return self.page_size

        try:
            value = int(page_size)
        except (TypeError, ValueError):
            raise ValidationError(
                {"page_size": "Must be an integer."}
            )

        if value <= 0:
            raise ValidationError(
                {"page_size": "Must be greater than zero."}
            )

        if value > self.max_page_size:
            raise ValidationError(
                {
                    "page_size": (
                        f"Must not be greater than "
                        f"{self.max_page_size}."
                    )
                }
            )

        return value
