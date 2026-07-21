"""
Tests for unsuccessful review list and creation requests.
"""

from django.urls import reverse
from rest_framework import status

from reviews_app.models import Review
from reviews_app.tests.base import ReviewsEndpointTestBase


class ReviewListCreateAPITestCaseUnhappy(
    ReviewsEndpointTestBase
):
    """
    Tests authentication, permission, and validation errors.
    """

    def test_unauthenticated_user_cannot_get_reviews(self):
        """
        Tests that unauthenticated review list requests return 401.
        """

        url = reverse("review-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_create_review(self):
        """
        Tests that unauthenticated review creation returns 401.
        """

        url = reverse("review-list")

        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_business_user_cannot_create_review(self):
        """
        Tests that a business user cannot create a review.
        """

        self.authenticate(
            self.business_token,
        )

        url = reverse("review-list")

        data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_customer_cannot_review_same_business_twice(self):
        """
        Tests that duplicate reviews for one business are rejected.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Noch eine Bewertung.",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            Review.objects.count(),
            2,
        )

    def test_customer_cannot_create_review_with_invalid_rating(
        self,
    ):
        """
        Tests that a rating outside the valid range is rejected.
        """

        self.authenticate(
            self.second_customer_token,
        )

        url = reverse("review-list")

        data = {
            "business_user": self.business_user.id,
            "rating": 6,
            "description": "Ungültiges Rating.",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(
            Review.objects.filter(
                reviewer=self.second_customer,
                business_user=self.business_user,
            ).exists()
        )
