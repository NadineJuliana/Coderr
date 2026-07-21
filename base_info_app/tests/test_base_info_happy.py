"""
Tests for the platform base information endpoint.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer
from reviews_app.models import Review


User = get_user_model()


class BaseInfoAPITestCaseHappy(APITestCase):
    """
    Tests successful requests for platform statistics.
    """

    def setUp(self):
        """
        Creates users, reviews, and offers for the statistics test.
        """

        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.other_customer_user = User.objects.create_user(
            username="other_customer_user",
            email="other_customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.other_business_user = User.objects.create_user(
            username="other_business_user",
            email="other_business@mail.de",
            password="examplePassword",
            type="business",
        )

        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Sehr guter Service.",
        )

        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.other_customer_user,
            rating=5,
            description="Top Qualität.",
        )

        Offer.objects.create(
            user=self.business_user,
            title="Webentwicklung",
            description="Professionelle Webentwicklung",
        )

        Offer.objects.create(
            user=self.other_business_user,
            title="Grafikdesign",
            description="Professionelles Grafikdesign",
        )

    def test_base_info_returns_platform_statistics(self):
        """
        Tests that the endpoint returns the expected statistics.
        """

        url = reverse("base-info")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data,
            {
                "review_count": 2,
                "average_rating": 4.5,
                "business_profile_count": 2,
                "offer_count": 2,
            },
        )
