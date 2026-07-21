from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from reviews_app.models import Review


User = get_user_model()


class ReviewsTestBase(APITestCase):

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

        self.second_customer_token = Token.objects.create(
            user=self.second_customer,
        )

        self.business_token = Token.objects.create(
            user=self.business_user,
        )

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

    def create_review(
        self,
        *,
        business_user=None,
        reviewer=None,
        rating=4,
        description="Sehr professioneller Service.",
    ):
        return Review.objects.create(
            business_user=business_user or self.business_user,
            reviewer=reviewer or self.customer_user,
            rating=rating,
            description=description,
        )


class ReviewsEndpointTestBase(ReviewsTestBase):

    def setUp(self):
        super().setUp()

        self.review = self.create_review()

        self.second_review = self.create_review(
            business_user=self.second_business_user,
            reviewer=self.second_customer,
            rating=5,
            description="Top Qualität und schnelle Lieferung!",
        )
