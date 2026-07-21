from django.urls import reverse
from rest_framework import status

from offers_app.tests.base import OffersEndpointTestBase


class OfferDetailObjectAPITestCaseUnhappy(
    OffersEndpointTestBase
):

    def test_unauthenticated_user_cannot_get_offer_detail_object(
        self,
    ):
        url = reverse(
            "offer-detail-object",
            kwargs={
                "pk": self.basic_detail.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_gets_404_for_missing_detail(
        self,
    ):
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "offer-detail-object",
            kwargs={
                "pk": 9999,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
