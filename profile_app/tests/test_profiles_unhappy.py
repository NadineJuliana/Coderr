from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profile_app.models import Profile


User = get_user_model()


class ProfileAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@mail.de",
            password="testpassword",
            type="customer",
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            email="otheruser@mail.de",
            password="otherpassword",
            type="business",
        )

        self.profile = Profile.objects.create(
            user=self.user,
        )

        self.other_profile = Profile.objects.create(
            user=self.other_user,
        )

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token.key
        )

    def test_patch_other_profile_returns_403(self):
        url = reverse(
            "profile-detail",
            kwargs={"pk": self.other_user.id},
        )

        data = {
            "first_name": "Changed Name",
            "location": "Berlin",
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

    def test_get_profile_without_authentication_returns_401(self):
        self.client.credentials()

        url = reverse(
            "profile-detail",
            kwargs={"pk": self.user.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_non_existing_profile_returns_404(self):
        url = reverse(
            "profile-detail",
            kwargs={"pk": 9999},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_get_business_profiles_without_authentication_returns_401(self):
        self.client.credentials()

        url = reverse("business-profile-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_get_customer_profiles_without_authentication_returns_401(self):
        self.client.credentials()

        url = reverse("customer-profile-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
