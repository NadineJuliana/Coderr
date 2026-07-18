from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


User = get_user_model()


class LoginAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.password = "examplePassword"

        self.user = User.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password=self.password,
            type="customer",
        )

        self.url = reverse("login")
        self.data = {
            "username": self.user.username,
            "password": self.password,
        }

    def test_login_returns_200(self):
        response = self.client.post(
            self.url,
            self.data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_login_returns_user_data_and_token(self):
        response = self.client.post(
            self.url,
            self.data,
            format="json",
        )

        token = Token.objects.get(user=self.user)

        expected_data = {
            "token": token.key,
            "username": self.user.username,
            "email": self.user.email,
            "user_id": self.user.id,
        }

        self.assertEqual(
            response.data,
            expected_data,
        )


class LoginAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="exampleUsername",
            email="example@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.url = reverse("login")
        self.data = {
            "username": self.user.username,
            "password": "wrongPassword",
        }

    def test_login_returns_400_for_invalid_data(self):
        response = self.client.post(
            self.url,
            self.data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
