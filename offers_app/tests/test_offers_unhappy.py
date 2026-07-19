from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


User = get_user_model()


class OffersAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.other_business_user = User.objects.create_user(
            username="other_business",
            email="other@mail.de",
            password="examplePassword",
            type="business",
        )

        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.business_token = Token.objects.create(
            user=self.business_user,
        )

        self.other_business_token = Token.objects.create(
            user=self.other_business_user,
        )

        self.customer_token = Token.objects.create(
            user=self.customer_user,
        )

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Website Design",
            description="Professionelles Website-Design",
        )

        self.basic_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=[
                "Logo Design",
                "Visitenkarte",
            ],
            offer_type="basic",
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Standard Design",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=[
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
            ],
            offer_type="standard",
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Premium Design",
            revisions=10,
            delivery_time_in_days=10,
            price=500,
            features=[
                "Logo Design",
                "Visitenkarte",
                "Briefpapier",
                "Flyer",
            ],
            offer_type="premium",
        )

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key,
        )

    def get_offer_data(self):
        return {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": (
                "Ein umfassendes Grafikdesign-Paket "
                "für Unternehmen."
            ),
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": [
                        "Logo Design",
                    ],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                    ],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": [
                        "Logo Design",
                        "Visitenkarte",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

    def test_unauthenticated_user_cannot_create_offer(self):
        url = reverse("offer-list")

        response = self.client.post(
            url,
            self.get_offer_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_user_cannot_create_offer(self):
        self.authenticate(
            self.customer_token,
        )

        url = reverse("offer-list")

        response = self.client.post(
            url,
            self.get_offer_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_offer_requires_exactly_three_details(self):
        self.authenticate(
            self.business_token,
        )

        url = reverse("offer-list")

        data = self.get_offer_data()
        data["details"] = data["details"][:2]

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn(
            "details",
            response.data,
        )

    def test_unauthenticated_user_cannot_get_offer_detail(self):
        url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_gets_404_for_missing_offer(self):
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "offer-detail",
            kwargs={"pk": 9999},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_non_owner_cannot_update_offer(self):
        self.authenticate(
            self.other_business_token,
        )

        url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        response = self.client.patch(
            url,
            {
                "title": "Nicht erlaubte Änderung",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_update_offer(self):
        url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        response = self.client.patch(
            url,
            {
                "title": "Nicht erlaubte Änderung",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_non_owner_cannot_delete_offer(self):
        self.authenticate(
            self.other_business_token,
        )

        url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Offer.objects.filter(
                id=self.offer.id,
            ).exists()
        )

    def test_unauthenticated_user_cannot_get_offer_detail_object(
        self,
    ):
        url = reverse(
            "offer-detail-object",
            kwargs={"pk": self.basic_detail.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_gets_404_for_missing_detail(
        self,
    ):
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "offer-detail-object",
            kwargs={"pk": 9999},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
