from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from offers_app.models import Offer
from reviews_app.models import Review


User = get_user_model()


class BaseInfoAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
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
            username="second_business_user",
            email="second_business@mail.de",
            password="examplePassword",
            type="business",
        )

        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=4,
            description="Sehr guter Service.",
        )

        self.second_customer = User.objects.create_user(
            username="second_customer",
            email="second_customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        Review.objects.create(
            business_user=self.business_user,
            reviewer=self.second_customer,
            rating=5,
            description="Top Qualität.",
        )

        Offer.objects.create(
            user=self.business_user,
            title="Webentwicklung",
            description="Professionelle Webentwicklung",
        )

        Offer.objects.create(
            user=self.second_business_user,
            title="Grafikdesign",
            description="Professionelles Grafikdesign",
        )

    def test_base_info_returns_platform_statistics(self):
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
