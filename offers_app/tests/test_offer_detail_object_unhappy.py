from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.tests.factories import (
    create_offer_with_details,
)


User = get_user_model()


class OfferDetailObjectAPITestCaseUnhappy(
    APITestCase
):

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

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=(
                "Token " + self.token.key
            ),
        )

    def test_unauthenticated_user_cannot_get_offer_detail_object(
        self,
    ):
        url = reverse(
            "offer-detail-object",
            kwargs={"pk": self.basic_detail.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_gets_404_for_missing_detail(
        self,
    ):
        self.authenticate()

        url = reverse(
            "offer-detail-object",
            kwargs={"pk": 9999},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
