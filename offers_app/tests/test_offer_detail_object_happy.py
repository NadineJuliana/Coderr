from django.urls import reverse
from rest_framework import status

from offers_app.tests.base import OffersEndpointTestBase


class OfferDetailObjectAPITestCaseHappy(
    OffersEndpointTestBase
):

    def setUp(self):
        super().setUp()

        self.url = reverse(
            "offer-detail-object",
            kwargs={
                "pk": self.basic_detail.id,
            },
        )

    def test_authenticated_user_can_get_offer_detail_object(
        self,
    ):
        self.authenticate(
            self.business_token,
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["id"],
            self.basic_detail.id,
        )
        self.assertEqual(
            response.data["title"],
            self.basic_detail.title,
        )
        self.assertEqual(
            response.data["revisions"],
            self.basic_detail.revisions,
        )
        self.assertEqual(
            response.data["delivery_time_in_days"],
            self.basic_detail.delivery_time_in_days,
        )
        self.assertEqual(
            response.data["price"],
            self.basic_detail.price,
        )
        self.assertEqual(
            response.data["features"],
            self.basic_detail.features,
        )
        self.assertEqual(
            response.data["offer_type"],
            self.basic_detail.offer_type,
        )
