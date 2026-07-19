from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


User = get_user_model()


class OffersAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            first_name="Max",
            last_name="Mustermann",
            type="business",
        )

        self.token = Token.objects.create(
            user=self.business_user,
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

        self.standard_detail = OfferDetail.objects.create(
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

        self.premium_detail = OfferDetail.objects.create(
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

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token.key
        )

    def test_get_offer_list_returns_offers(self):
        url = reverse("offer-list")

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
            response.data[0]["id"],
            self.offer.id,
        )
        self.assertEqual(
            response.data[0]["user"],
            self.business_user.id,
        )
        self.assertEqual(
            response.data[0]["min_price"],
            100,
        )
        self.assertEqual(
            response.data[0]["min_delivery_time"],
            5,
        )
        self.assertEqual(
            len(response.data[0]["details"]),
            3,
        )

    def test_get_offer_list_supports_query_parameters(self):
        second_user = User.objects.create_user(
            username="second_business",
            email="second@mail.de",
            password="examplePassword",
            type="business",
        )

        second_offer = Offer.objects.create(
            user=second_user,
            title="Logo Design",
            description="Individuelles Logo für Unternehmen",
        )

        OfferDetail.objects.create(
            offer=second_offer,
            title="Basic Logo",
            revisions=1,
            delivery_time_in_days=3,
            price=50,
            features=["Logo"],
            offer_type="basic",
        )

        OfferDetail.objects.create(
            offer=second_offer,
            title="Standard Logo",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo", "Visitenkarte"],
            offer_type="standard",
        )

        OfferDetail.objects.create(
            offer=second_offer,
            title="Premium Logo",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=["Logo", "Visitenkarte", "Briefpapier"],
            offer_type="premium",
        )

        url = reverse("offer-list")

        response = self.client.get(
            url,
            {
                "creator_id": second_user.id,
                "min_price": 50,
                "max_delivery_time": 3,
                "search": "Logo",
                "ordering": "min_price",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            1,
        )
        self.assertEqual(
            response.data[0]["id"],
            second_offer.id,
        )

    def test_business_user_can_create_offer(self):
        self.authenticate()

        url = reverse("offer-list")

        data = {
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
                        "Visitenkarte",
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
                        "Briefpapier",
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
                        "Briefpapier",
                        "Flyer",
                    ],
                    "offer_type": "premium",
                },
            ],
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Offer.objects.count(),
            2,
        )
        self.assertEqual(
            response.data["title"],
            data["title"],
        )
        self.assertEqual(
            len(response.data["details"]),
            3,
        )
        self.assertEqual(
            response.data["details"][0]["offer_type"],
            "basic",
        )
        self.assertEqual(
            response.data["details"][1]["offer_type"],
            "standard",
        )
        self.assertEqual(
            response.data["details"][2]["offer_type"],
            "premium",
        )

    def test_authenticated_user_can_get_offer_detail(self):
        self.authenticate()

        url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["id"],
            self.offer.id,
        )
        self.assertEqual(
            response.data["user"],
            self.business_user.id,
        )
        self.assertEqual(
            response.data["title"],
            self.offer.title,
        )
        self.assertEqual(
            len(response.data["details"]),
            3,
        )
        self.assertEqual(
            response.data["min_price"],
            100,
        )
        self.assertEqual(
            response.data["min_delivery_time"],
            5,
        )

    def test_owner_can_update_offer(self):
        self.authenticate()

        url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        data = {
            "title": "Updated Website Design",
            "details": [
                {
                    "title": "Updated Basic Design",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo Design",
                        "Flyer",
                    ],
                    "offer_type": "basic",
                },
            ],
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
            response.data["title"],
            data["title"],
        )
        self.assertEqual(
            len(response.data["details"]),
            3,
        )

        updated_basic_detail = next(
            detail
            for detail in response.data["details"]
            if detail["offer_type"] == "basic"
        )

        self.assertEqual(
            updated_basic_detail["id"],
            self.basic_detail.id,
        )
        self.assertEqual(
            updated_basic_detail["title"],
            "Updated Basic Design",
        )
        self.assertEqual(
            updated_basic_detail["price"],
            120,
        )

    def test_owner_can_delete_offer(self):
        self.authenticate()

        url = reverse(
            "offer-detail",
            kwargs={"pk": self.offer.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Offer.objects.filter(
                id=self.offer.id,
            ).exists()
        )

    def test_authenticated_user_can_get_offer_detail_object(self):
        self.authenticate()

        url = reverse(
            "offer-detail-object",
            kwargs={"pk": self.basic_detail.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["id"],
            self.basic_detail.id,
        )
        self.assertEqual(
            response.data["title"],
            self.basic_detail.title,
        )
        self.assertEqual(
            response.data["revisions"],
            self.basic_detail.revisions,
        )
        self.assertEqual(
            response.data["delivery_time_in_days"],
            self.basic_detail.delivery_time_in_days,
        )
        self.assertEqual(
            response.data["price"],
            100,
        )
        self.assertEqual(
            response.data["features"],
            self.basic_detail.features,
        )
        self.assertEqual(
            response.data["offer_type"],
            self.basic_detail.offer_type,
        )
