"""
Tests for successful review list and creation requests.
"""

from django.urls import reverse
from rest_framework import status

from reviews_app.models import Review
from reviews_app.tests.base import ReviewsEndpointTestBase


class ReviewListCreateAPITestCaseHappy(
    ReviewsEndpointTestBase
):
    """
    Tests successful review listing, filtering, and creation.
    """

    def test_authenticated_user_can_get_reviews(self):
        """
        Tests that an authenticated user can retrieve reviews.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            2,
        )
        self.assertEqual(
            response.data[0]["business_user"],
            self.business_user.id,
        )
        self.assertEqual(
            response.data[0]["reviewer"],
            self.customer_user.id,
        )

    def test_reviews_can_be_filtered_by_business_user(self):
        """
        Tests filtering reviews by business user.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        response = self.client.get(
            url,
            {
                "business_user_id": self.business_user.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            1,
        )
        self.assertEqual(
            response.data[0]["id"],
            self.review.id,
        )

    def test_reviews_can_be_filtered_by_reviewer(self):
        """
        Tests filtering reviews by reviewer.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        response = self.client.get(
            url,
            {
                "reviewer_id": self.customer_user.id,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            1,
        )
        self.assertEqual(
            response.data[0]["id"],
            self.review.id,
        )

    def test_reviews_can_be_ordered_by_rating(self):
        """
        Tests ordering reviews by rating.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        response = self.client.get(
            url,
            {
                "ordering": "rating",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data[0]["rating"],
            4,
        )
        self.assertEqual(
            response.data[1]["rating"],
            5,
        )

    def test_reviews_can_be_ordered_by_updated_at(self):
        """
        Tests ordering reviews by their last update time.
        """

        self.review.description = "Aktualisierte Bewertung"
        self.review.save()

        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        response = self.client.get(
            url,
            {
                "ordering": "updated_at",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data[-1]["id"],
            self.review.id,
        )

    def test_customer_can_create_review(self):
        """
        Tests that a customer can create a review.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        data = {
            "business_user": self.second_business_user.id,
            "rating": 5,
            "description": "Alles war toll!",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Review.objects.count(),
            3,
        )
        self.assertEqual(
            response.data["business_user"],
            self.second_business_user.id,
        )
        self.assertEqual(
            response.data["reviewer"],
            self.customer_user.id,
        )
        self.assertEqual(
            response.data["rating"],
            5,
        )
        self.assertEqual(
            response.data["description"],
            "Alles war toll!",
        )
