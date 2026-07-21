"""
Views for listing, creating, updating, and deleting reviews.
"""

from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from reviews_app.models import Review

from .filters import ReviewFilter
from .permissions import (
    IsCustomerForCreate,
    IsReviewAuthor,
)
from .serializers import (
    ReviewCreateSerializer,
    ReviewSerializer,
)


# Create your views here.

class ReviewListCreateView(ListCreateAPIView):
    """
    Lists reviews and allows customers to create new reviews.
    """

    queryset = Review.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_class = ReviewFilter

    ordering_fields = [
        "updated_at",
        "rating",
    ]

    def get_serializer_class(self):
        """
        Returns the serializer matching the request method.
        """

        if self.request.method == "POST":
            return ReviewCreateSerializer

        return ReviewSerializer

    def get_permissions(self):
        """
        Adds the customer permission to review creation requests.
        """

        permissions = [
            IsAuthenticated(),
        ]

        if self.request.method == "POST":
            permissions.append(
                IsCustomerForCreate(),
            )

        return permissions


class ReviewDetailView(
    RetrieveUpdateDestroyAPIView
):
    """
    Allows review authors to update or delete their reviews.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticated,
        IsReviewAuthor,
    ]

    http_method_names = [
        "patch",
        "delete",
        "head",
        "options",
    ]
