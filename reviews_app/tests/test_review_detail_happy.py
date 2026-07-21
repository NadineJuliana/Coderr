from django.urls import reverse
from rest_framework import status

from reviews_app.models import Review
from reviews_app.tests.base import ReviewsEndpointTestBase


class ReviewDetailAPITestCaseHappy(
    ReviewsEndpointTestBase
):

    def test_reviewer_can_update_own_review(self):
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
            "rating": 5,
            "description": "Noch besser als erwartet!",
        }

        response = self.client.patch(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["rating"],
            5,
        )
        self.assertEqual(
            response.data["description"],
            "Noch besser als erwartet!",
        )

        self.review.refresh_from_db()

        self.assertEqual(
            self.review.rating,
            5,
        )

    def test_reviewer_can_delete_own_review(self):
        self.authenticate(
            self.customer_token,
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
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Review.objects.filter(
                id=self.review.id,
            ).exists()
        )
