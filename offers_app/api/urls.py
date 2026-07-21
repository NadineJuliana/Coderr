"""
URL routes for offer endpoints.
"""

from django.urls import path
from .views import (
    OfferListCreateView,
    OfferDetailView,
    OfferDetailObjectView,
)

urlpatterns = [
    path(
        "offers/",
        OfferListCreateView.as_view(),
        name="offer-list",
    ),
    path(
        "offers/<int:pk>/",
        OfferDetailView.as_view(),
        name="offer-detail",
    ),
    path(
        "offerdetails/<int:pk>/",
        OfferDetailObjectView.as_view(),
        name="offer-detail-object",
    )
]
