from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.tests.factories import (
    create_offer_with_details,
)


User = get_user_model()


class OfferDetailObjectAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
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
            "offer-detail-object",
            kwargs={"pk": self.basic_detail.id},
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                "Token " + self.token.key
            ),
        )

    def test_authenticated_user_can_get_offer_detail_object(
        self,
    ):
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
