from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.tests.factories import (
    get_valid_offer_data,
)


User = get_user_model()


class OfferListAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.business_token = Token.objects.create(
            user=self.business_user,
        )

        self.customer_token = Token.objects.create(
            user=self.customer_user,
        )

        self.url = reverse("offer-list")

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=(
                "Token " + token.key
            ),
        )

    def test_unauthenticated_user_cannot_create_offer(self):
        response = self.client.post(
            self.url,
            get_valid_offer_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_user_cannot_create_offer(self):
        self.authenticate(
            self.customer_token,
        )

        response = self.client.post(
            self.url,
            get_valid_offer_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_offer_requires_exactly_three_details(self):
        self.authenticate(
            self.business_token,
        )

        data = get_valid_offer_data()
        data["details"] = data["details"][:2]

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn(
            "details",
            response.data,
        )

    def test_get_offer_list_with_invalid_query_returns_400(
        self,
    ):
        response = self.client.get(
            self.url,
            {
                "min_price": "invalid",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
