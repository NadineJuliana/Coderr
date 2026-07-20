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


class OfferDetailAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.other_business_user = User.objects.create_user(
            username="other_business",
            email="other@mail.de",
            password="examplePassword",
            type="business",
        )

        self.business_token = Token.objects.create(
            user=self.business_user,
        )

        self.other_business_token = Token.objects.create(
            user=self.other_business_user,
        )

        (
            self.offer,
            self.basic_detail,
            self.standard_detail,
            self.premium_detail,
        ) = create_offer_with_details(
            self.business_user,
        )

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=(
                "Token " + token.key
            ),
        )

    def get_offer_url(self, offer_id):
        return reverse(
            "offer-detail",
            kwargs={"pk": offer_id},
        )

    def test_unauthenticated_user_cannot_get_offer_detail(
        self,
    ):
        url = self.get_offer_url(
            self.offer.id,
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_gets_404_for_missing_offer(
        self,
    ):
        self.authenticate(
            self.business_token,
        )

        url = self.get_offer_url(9999)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_non_owner_cannot_update_offer(self):
        self.authenticate(
            self.other_business_token,
        )

        url = self.get_offer_url(
            self.offer.id,
        )

        response = self.client.patch(
            url,
            {
                "title": "Nicht erlaubte Änderung",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_update_offer(
        self,
    ):
        url = self.get_offer_url(
            self.offer.id,
        )

        response = self.client.patch(
            url,
            {
                "title": "Nicht erlaubte Änderung",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_update_missing_offer_returns_404(self):
        self.authenticate(
            self.business_token,
        )

        url = self.get_offer_url(9999)

        response = self.client.patch(
            url,
            {
                "title": "Updated title",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_update_offer_with_invalid_data_returns_400(
        self,
    ):
        self.authenticate(
            self.business_token,
        )

        url = self.get_offer_url(
            self.offer.id,
        )

        response = self.client.patch(
            url,
            {
                "details": [
                    {
                        "title": "Invalid Detail",
                        "revisions": 2,
                        "delivery_time_in_days": 5,
                        "price": 100,
                        "features": [
                            "Logo Design",
                        ],
                    },
                ],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_non_owner_cannot_delete_offer(self):
        self.authenticate(
            self.other_business_token,
        )

        url = self.get_offer_url(
            self.offer.id,
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Offer.objects.filter(
                id=self.offer.id,
            ).exists()
        )

    def test_unauthenticated_user_cannot_delete_offer(
        self,
    ):
        url = self.get_offer_url(
            self.offer.id,
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertTrue(
            Offer.objects.filter(
                id=self.offer.id,
            ).exists()
        )

    def test_delete_missing_offer_returns_404(self):
        self.authenticate(
            self.business_token,
        )

        url = self.get_offer_url(9999)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
