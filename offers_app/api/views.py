from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from offers_app.models import Offer, OfferDetail
from .pagination import OfferPagination
from .filters import OfferFilter
from .permissions import (
    IsBusinessUser,
    IsOfferOwnerOrReadOnly,
)
from .serializers import (
    OfferDetailObjectSerializer,
    OfferListSerializer,
    OfferRetrieveSerializer,
    OfferWriteSerializer,
)


# Create your views here.


class OfferListCreateView(ListCreateAPIView):
    queryset = Offer.objects.annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min(
            "details__delivery_time_in_days",
        ),
    )

    pagination_class = OfferPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = OfferFilter

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "updated_at",
        "min_price",
    ]

    ordering = ["-updated_at"]

    valid_ordering_fields = {
        "updated_at",
        "-updated_at",
        "min_price",
        "-min_price",
    }

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferWriteSerializer

        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsAuthenticated(),
            IsBusinessUser(),
        ]

    def list(self, request, *args, **kwargs):
        self.validate_ordering(request)

        return super().list(
            request,
            *args,
            **kwargs,
        )

    def validate_ordering(self, request):
        ordering = request.query_params.get("ordering")

        if (
            ordering
            and ordering not in self.valid_ordering_fields
        ):
            raise ValidationError(
                {
                    "ordering": (
                        "Invalid ordering parameter."
                    )
                }
            )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
        )


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.annotate(
        min_price=Min("details__price"),
        min_delivery_time=Min(
            "details__delivery_time_in_days",
        ),
    )

    permission_classes = [
        IsAuthenticated,
        IsOfferOwnerOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OfferRetrieveSerializer

        return OfferWriteSerializer


class OfferDetailObjectView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()

    serializer_class = OfferDetailObjectSerializer

    permission_classes = [
        IsAuthenticated,
    ]
