"""
Tests for unsuccessful review detail endpoint requests.
"""

from django.urls import reverse
from rest_framework import status

from reviews_app.models import Review
from reviews_app.tests.base import ReviewsEndpointTestBase


class ReviewDetailAPITestCaseUnhappy(
    ReviewsEndpointTestBase
):
    """
    Tests authentication, permission, and missing review errors.
    """

    def test_unauthenticated_user_cannot_update_review(self):
        """
        Tests that unauthenticated review updates return status 401.
        """

        url = reverse(
            "review-detail",
            kwargs={
                "pk": self.review.id,
            },
        )

        data = {
            "rating": 5,
        }

        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_other_customer_cannot_update_review(self):
        """
        Tests that another customer cannot update the review.
        """

        self.authenticate(
            self.second_customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={
                "pk": self.review.id,
            },
        )

        data = {
            "rating": 5,
            "description": "Fremde Änderung.",
        }

        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_reviewer_cannot_update_business_user(self):
        """
        Tests that the reviewed business user cannot be changed.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={
                "pk": self.review.id,
            },
        )

        data = {
            "business_user": self.second_business_user.id,
        }

        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.review.refresh_from_db()

        self.assertEqual(
            self.review.business_user,
            self.business_user,
        )

    def test_update_nonexistent_review_returns_not_found(self):
        """
        Tests that updating a missing review returns status 404.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={
                "pk": 99999,
            },
        )

        data = {
            "rating": 5,
        }

        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_delete_review(self):
        """
        Tests that unauthenticated review deletion returns status 401.
        """

        url = reverse(
            "review-detail",
            kwargs={
                "pk": self.review.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_other_customer_cannot_delete_review(self):
        """
        Tests that another customer cannot delete the review.
        """

        self.authenticate(
            self.second_customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={
                "pk": self.review.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Review.objects.filter(
                id=self.review.id,
            ).exists()
        )

    def test_delete_nonexistent_review_returns_not_found(self):
        """
        Tests that deleting a missing review returns status 404.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={
                "pk": 99999,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
