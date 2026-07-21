"""
Tests for unsuccessful offer detail endpoint requests.
"""

from django.urls import reverse
from rest_framework import status

from offers_app.models import Offer
from offers_app.tests.base import OffersEndpointTestBase


class OfferDetailAPITestCaseUnhappy(
    OffersEndpointTestBase
):
    """
    Tests authentication, permission, validation, and missing offer errors.
    """

    def get_offer_url(self, offer_id):
        """
        Returns the detail URL for the provided offer ID.
        """

        return reverse(
            "offer-detail",
            kwargs={
                "pk": offer_id,
            },
        )

    def test_unauthenticated_user_cannot_get_offer_detail(
        self,
    ):
        """
        Tests that unauthenticated offer requests return status 401.
        """

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
        """
        Tests that requesting a missing offer returns status 404.
        """

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
        """
        Tests that a non-owner cannot update an offer.
        """

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
        """
        Tests that unauthenticated offer updates return status 401.
        """

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
        """
        Tests that updating a missing offer returns status 404.
        """

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
        """
        Tests that invalid offer update data returns status 400.
        """

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
        """
        Tests that a non-owner cannot delete an offer.
        """

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
        """
        Tests that unauthenticated offer deletion returns status 401.
        """

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
        """
        Tests that deleting a missing offer returns status 404.
        """

        self.authenticate(
            self.business_token,
        )

        url = self.get_offer_url(9999)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
