from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from reviews_app.models import Review


User = get_user_model()


class ReviewsAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.second_customer = User.objects.create_user(
            username="second_customer",
            email="second_customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.second_business_user = User.objects.create_user(
            username="second_business",
            email="second_business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.customer_token = Token.objects.create(
            user=self.customer_user,
        )

        self.business_token = Token.objects.create(
            user=self.business_user,
        )

        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Sehr professioneller Service.",
        )

        self.second_review = Review.objects.create(
            business_user=self.second_business_user,
            reviewer=self.second_customer,
            rating=5,
            description="Top Qualität und schnelle Lieferung!",
        )

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

    def test_authenticated_user_can_get_reviews(self):
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
        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        response = self.client.get(
            url,
            {
                "business_user_id": (
                    self.business_user.id
                ),
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
        self.review.description = (
            "Aktualisierte Bewertung"
        )
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
        self.authenticate(
            self.customer_token,
        )

        url = reverse("review-list")

        data = {
            "business_user": (
                self.second_business_user.id
            ),
            "rating": 5,
            "description": (
                "Alles war toll!"
            ),
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

    def test_reviewer_can_update_own_review(self):
        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={"pk": self.review.id},
        )

        data = {
            "rating": 5,
            "description": (
                "Noch besser als erwartet!"
            ),
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
            kwargs={"pk": self.review.id},
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
