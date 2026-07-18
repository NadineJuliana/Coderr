from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


User = get_user_model()


class RegistrationAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.url = reverse("registration")
        self.data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def test_registration_creates_user_and_returns_201(self):
        response = self.client.post(
            self.url,
            self.data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertTrue(
            User.objects.filter(
                username=self.data["username"]
            ).exists()
        )

    def test_registration_returns_user_data_and_token(self):
        response = self.client.post(
            self.url,
            self.data,
            format="json",
        )

        user = User.objects.get(
            username=self.data["username"]
        )
        token = Token.objects.get(user=user)

        expected_data = {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }

        self.assertEqual(
            response.data,
            expected_data,
        )


class RegistrationAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.url = reverse("registration")
        self.data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "differentPassword",
            "type": "customer",
        }

    def test_registration_returns_400_for_invalid_data(self):
        response = self.client.post(
            self.url,
            self.data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
