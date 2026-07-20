from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profile_app.models import Profile


User = get_user_model()


class ProfileAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="max_mustermann",
            email="max@business.de",
            password="examplePassword",
            first_name="Max",
            last_name="Mustermann",
            type="business",
        )

        self.profile = Profile.objects.create(
            user=self.user,
            location="Berlin",
            tel="123456789",
            description="Business description",
            working_hours="9-17",
        )

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token.key
        )

    def test_get_profile_detail(self):
        url = reverse(
            "profile-detail",
            kwargs={"pk": self.user.id},
        )

        response = self.client.get(url)

        expected_data = {
            "user": self.user.id,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "file": None,
            "location": self.profile.location,
            "tel": self.profile.tel,
            "description": self.profile.description,
            "working_hours": self.profile.working_hours,
            "type": self.user.type,
            "email": self.user.email,
            "created_at": response.data["created_at"],
        }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data,
            expected_data,
        )

    def test_patch_own_profile(self):
        url = reverse(
            "profile-detail",
            kwargs={"pk": self.user.id},
        )

        data = {
            "first_name": "Updated Max",
            "last_name": "Updated Mustermann",
            "location": "München",
            "tel": "987654321",
            "description": "Updated business description",
            "working_hours": "10-18",
            "email": "new_email@business.de",
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
            response.data["first_name"],
            data["first_name"],
        )
        self.assertEqual(
            response.data["last_name"],
            data["last_name"],
        )
        self.assertEqual(
            response.data["location"],
            data["location"],
        )
        self.assertEqual(
            response.data["tel"],
            data["tel"],
        )
        self.assertEqual(
            response.data["description"],
            data["description"],
        )
        self.assertEqual(
            response.data["working_hours"],
            data["working_hours"],
        )
        self.assertEqual(
            response.data["email"],
            data["email"],
        )

    def test_get_business_profile_list(self):
        customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        Profile.objects.create(
            user=customer_user,
            location="Hamburg",
        )

        url = reverse("business-profile-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            1,
        )
        self.assertEqual(
            response.data[0]["user"],
            self.user.id,
        )
        self.assertEqual(
            response.data[0]["type"],
            "business",
        )

    def test_get_customer_profile_list(self):
        customer_user = User.objects.create_user(
            username="customer_jane",
            email="customer@mail.de",
            password="examplePassword",
            first_name="Jane",
            last_name="Doe",
            type="customer",
        )

        Profile.objects.create(
            user=customer_user,
        )

        url = reverse("customer-profile-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            1,
        )
        self.assertEqual(
            response.data[0]["user"],
            customer_user.id,
        )
        self.assertEqual(
            response.data[0]["type"],
            "customer",
        )
        self.assertEqual(
            response.data[0]["first_name"],
            customer_user.first_name,
        )
        self.assertEqual(
            response.data[0]["last_name"],
            customer_user.last_name,
        )

    def test_get_profile_detail_returns_empty_strings_for_empty_fields(self):
        user = User.objects.create_user(
            username="empty_user",
            email="empty@mail.de",
            password="examplePassword",
            type="customer",
        )

        Profile.objects.create(user=user)

        url = reverse(
            "profile-detail",
            kwargs={"pk": user.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        fields = [
            "first_name",
            "last_name",
            "location",
            "tel",
            "description",
            "working_hours",
        ]

        for field in fields:
            self.assertEqual(
                response.data[field],
                "",
            )
