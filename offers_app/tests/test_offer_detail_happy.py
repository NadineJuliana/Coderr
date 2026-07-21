from django.urls import reverse
from rest_framework import status

from offers_app.models import Offer
from offers_app.tests.base import OffersEndpointTestBase


class OfferDetailAPITestCaseHappy(
    OffersEndpointTestBase
):

    def setUp(self):
        super().setUp()

        self.url = reverse(
            "offer-detail",
            kwargs={
                "pk": self.offer.id,
            },
        )

    def test_authenticated_user_can_get_offer_detail(self):
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
            self.offer.id,
        )
        self.assertEqual(
            response.data["user"],
            self.business_user.id,
        )
        self.assertEqual(
            response.data["title"],
            self.offer.title,
        )
        self.assertEqual(
            len(response.data["details"]),
            3,
        )
        self.assertEqual(
            response.data["min_price"],
            100,
        )
        self.assertEqual(
            response.data["min_delivery_time"],
            5,
        )

    def test_owner_can_update_offer(self):
        self.authenticate(
            self.business_token,
        )

        data = {
            "title": "Updated Website Design",
            "details": [
                {
                    "title": "Updated Basic Design",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo Design",
                        "Flyer",
                    ],
                    "offer_type": "basic",
                },
            ],
        }

        response = self.client.patch(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertNotIn(
            "user",
            response.data,
        )
        self.assertEqual(
            response.data["title"],
            data["title"],
        )
        self.assertEqual(
            len(response.data["details"]),
            3,
        )

        updated_basic_detail = next(
            detail
            for detail in response.data["details"]
            if detail["offer_type"] == "basic"
        )

        self.assertEqual(
            updated_basic_detail["id"],
            self.basic_detail.id,
        )
        self.assertEqual(
            updated_basic_detail["title"],
            "Updated Basic Design",
        )
        self.assertEqual(
            updated_basic_detail["price"],
            120,
        )

    def test_owner_can_delete_offer(self):
        self.authenticate(
            self.business_token,
        )

        response = self.client.delete(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Offer.objects.filter(
                id=self.offer.id,
            ).exists()
        )
