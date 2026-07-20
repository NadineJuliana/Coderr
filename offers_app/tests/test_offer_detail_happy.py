from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer
from offers_app.tests.factories import (
    create_offer_with_details,
)


User = get_user_model()


class OfferDetailAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            first_name="Max",
            last_name="Mustermann",
            type="business",
        )

        self.token = Token.objects.create(
            user=self.business_user,
        )

        (
            self.offer,
            self.basic_detail,
            self.standard_detail,
            self.premium_detail,
        ) = create_offer_with_details(
            self.business_user,
        )

        self.url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                "Token " + self.token.key
            ),
        )

    def test_authenticated_user_can_get_offer_detail(self):
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
