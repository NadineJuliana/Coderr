"""
Tests for unsuccessful offer list and creation requests.
"""

from django.urls import reverse
from rest_framework import status

from offers_app.tests.base import OffersEndpointTestBase


class OfferListCreateAPITestCaseUnhappy(
    OffersEndpointTestBase
):
    """
    Tests authentication, permission, and validation errors.
    """

    def setUp(self):
        """
        Creates the shared test data and offer list URL.
        """

        super().setUp()

        self.url = reverse("offer-list")

    def test_unauthenticated_user_cannot_create_offer(self):
        """
        Tests that unauthenticated offer creation returns status 401.
        """

        response = self.client.post(
            self.url,
            self.get_valid_offer_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_user_cannot_create_offer(self):
        """
        Tests that a customer user cannot create an offer.
        """

        self.authenticate(
            self.customer_token,
        )

        response = self.client.post(
            self.url,
            self.get_valid_offer_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_offer_requires_exactly_three_details(self):
        """
        Tests that an offer requires exactly three details.
        """

        self.authenticate(
            self.business_token,
        )

        data = self.get_valid_offer_data()
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
        """
        Tests that an invalid filter value returns status 400.
        """

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
