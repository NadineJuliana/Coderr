from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from reviews_app.models import Review


User = get_user_model()


class ReviewsAPITestCaseUnhappy(APITestCase):

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

        self.customer_token = Token.objects.create(
            user=self.customer_user,
        )

        self.second_customer_token = Token.objects.create(
            user=self.second_customer,
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

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

    def test_unauthenticated_user_cannot_get_reviews(self):
        url = reverse("review-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_create_review(self):
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
            1,
        )

    def test_customer_cannot_create_review_with_invalid_rating(self):
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
            ).exists()
        )

    def test_unauthenticated_user_cannot_update_review(self):
        url = reverse(
            "review-detail",
            kwargs={"pk": self.review.id},
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
        self.authenticate(
            self.second_customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={"pk": self.review.id},
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
        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={"pk": self.review.id},
        )

        data = {
            "business_user": self.customer_user.id,
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
        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={"pk": 99999},
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
        url = reverse(
            "review-detail",
            kwargs={"pk": self.review.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_other_customer_cannot_delete_review(self):
        self.authenticate(
            self.second_customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={"pk": self.review.id},
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
        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "review-detail",
            kwargs={"pk": 99999},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
