"""
Views for retrieving general platform statistics.
"""

from django.contrib.auth import get_user_model
from django.db.models import Avg
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from offers_app.models import Offer
from reviews_app.models import Review


User = get_user_model()

# Create your views here.


class BaseInfoView(APIView):
    """
    Provides general statistics about the platform.
    """

    permission_classes = [
        AllowAny,
    ]

    def get(self, request):
        """
        Returns review, rating, business profile, and offer statistics.
        """

        review_count = Review.objects.count()

        average_rating = Review.objects.aggregate(
            average=Avg("rating"),
        )["average"]

        business_profile_count = User.objects.filter(
            type="business",
        ).count()

        offer_count = Offer.objects.count()

        return Response(
            {
                "review_count": review_count,
                "average_rating": round(
                    average_rating or 0,
                    1,
                ),
                "business_profile_count": (
                    business_profile_count
                ),
                "offer_count": offer_count,
            }
        )
