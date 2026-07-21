from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from offers_app.tests.factories import (
    create_offer_with_details,
    get_valid_offer_data,
)


User = get_user_model()


class OfferListAPITestCaseHappy(APITestCase):

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

        (
            self.offer,
            self.basic_detail,
            self.standard_detail,
            self.premium_detail,
        ) = create_offer_with_details(
            self.business_user,
        )

        self.url = reverse("offer-list")

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=(
                "Token " + self.token.key
            ),
        )

    def test_get_offer_list_returns_offers(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["count"],
            1,
        )
        self.assertIsNone(
            response.data["next"],
        )
        self.assertIsNone(
            response.data["previous"],
        )

        offer_data = response.data["results"][0]

        self.assertEqual(
            offer_data["id"],
            self.offer.id,
        )
        self.assertEqual(
            offer_data["user"],
            self.business_user.id,
        )
        self.assertEqual(
            offer_data["min_price"],
            100,
        )
        self.assertEqual(
            offer_data["min_delivery_time"],
            5,
        )
        self.assertEqual(
            len(offer_data["details"]),
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
            description=(
                "Individuelles Logo für Unternehmen"
            ),
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
            features=[
                "Logo",
                "Visitenkarte",
            ],
            offer_type="standard",
        )

        OfferDetail.objects.create(
            offer=second_offer,
            title="Premium Logo",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=[
                "Logo",
                "Visitenkarte",
                "Briefpapier",
            ],
            offer_type="premium",
        )

        response = self.client.get(
            self.url,
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
            response.data["count"],
            1,
        )
        self.assertEqual(
            response.data["results"][0]["id"],
            second_offer.id,
        )

    def test_get_offer_list_supports_page_size(self):
        response = self.client.get(
            self.url,
            {
                "page_size": 1,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data["results"]),
            1,
        )

    def test_business_user_can_create_offer(self):
        self.authenticate()

        data = get_valid_offer_data()

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertNotIn(
            "user",
            response.data,
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
