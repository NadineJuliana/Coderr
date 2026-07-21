"""
Tests for successful offer list and creation requests.
"""

from django.urls import reverse
from rest_framework import status

from offers_app.models import Offer
from offers_app.tests.base import OffersEndpointTestBase


class OfferListCreateAPITestCaseHappy(
    OffersEndpointTestBase
):
    """
    Tests successful offer listing, filtering, and creation.
    """

    def setUp(self):
        """
        Creates the shared test data and offer list URL.
        """

        super().setUp()

        self.url = reverse("offer-list")

    def test_get_offer_list_returns_offers(self):
        """
        Tests that the offer list returns paginated offers.
        """

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )
        self.assertIsNone(
            response.data["next"],
        )
        self.assertIsNone(
            response.data["previous"],
        )

        offer_data = response.data["results"][0]

        self.assertEqual(
            offer_data["id"],
            self.offer.id,
        )
        self.assertEqual(
            offer_data["user"],
            self.business_user.id,
        )
        self.assertEqual(
            offer_data["min_price"],
            100,
        )
        self.assertEqual(
            offer_data["min_delivery_time"],
            5,
        )
        self.assertEqual(
            len(offer_data["details"]),
            3,
        )

    def test_get_offer_list_supports_query_parameters(self):
        """
        Tests filtering, searching, and ordering the offer list.
        """

        (
            other_offer,
            other_basic_detail,
            _,
            _,
        ) = self.create_offer_with_details(
            user=self.other_business_user,
            title="Logo Design",
            description=(
                "Individuelles Logo für Unternehmen"
            ),
        )

        other_basic_detail.title = "Basic Logo"
        other_basic_detail.revisions = 1
        other_basic_detail.delivery_time_in_days = 3
        other_basic_detail.price = 50
        other_basic_detail.features = ["Logo"]
        other_basic_detail.save()

        response = self.client.get(
            self.url,
            {
                "creator_id": self.other_business_user.id,
                "min_price": 50,
                "max_delivery_time": 3,
                "search": "Logo",
                "ordering": "min_price",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )
        self.assertEqual(
            response.data["results"][0]["id"],
            other_offer.id,
        )

    def test_get_offer_list_supports_page_size(self):
        """
        Tests that the offer list supports a custom page size.
        """

        response = self.client.get(
            self.url,
            {
                "page_size": 1,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data["results"]),
            1,
        )

    def test_business_user_can_create_offer(self):
        """
        Tests that a business user can create an offer.
        """

        self.authenticate(
            self.business_token,
        )

        data = self.get_valid_offer_data()

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertNotIn(
            "user",
            response.data,
        )
        self.assertEqual(
            Offer.objects.count(),
            2,
        )
        self.assertEqual(
            response.data["title"],
            data["title"],
        )
        self.assertEqual(
            len(response.data["details"]),
            3,
        )
        self.assertEqual(
            response.data["details"][0]["offer_type"],
            "basic",
        )
        self.assertEqual(
            response.data["details"][1]["offer_type"],
            "standard",
        )
        self.assertEqual(
            response.data["details"][2]["offer_type"],
            "premium",
        )
