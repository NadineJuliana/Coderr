"""
Tests for the login endpoint.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


User = get_user_model()


class LoginAPITestCaseHappy(APITestCase):
    """
    Tests successful login requests.
    """

    def setUp(self):
        """
        Creates a user and prepares valid login data.
        """

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
        """
        Tests that a successful login returns status 200.
        """

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
        """
        Tests that login returns the user data and token.
        """

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
    """
    Tests unsuccessful login requests.
    """

    def setUp(self):
        """
        Creates a user and prepares invalid login data.
        """

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
        """
        Tests that invalid credentials return status 400.
        """

        response = self.client.post(
            self.url,
            self.data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
