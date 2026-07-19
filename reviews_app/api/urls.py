from django.urls import include, path
from .views import (
    ReviewDetailView,
    ReviewListCreateView,
)


urlpatterns = [
    path(
        "reviews/",
        ReviewListCreateView.as_view(),
        name="review-list",
    ),
    path(
        "reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="review-detail",
    ),
]
