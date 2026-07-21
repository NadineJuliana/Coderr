from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail


User = get_user_model()


class OffersTestBase(APITestCase):

    def setUp(self):
        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            first_name="Max",
            last_name="Mustermann",
            type="business",
        )

        self.other_business_user = User.objects.create_user(
            username="other_business_user",
            email="other_business@mail.de",
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

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

    def create_offer_with_details(
        self,
        *,
        user=None,
        title="Website Design",
        description="Professionelles Website-Design",
    ):
        offer = Offer.objects.create(
            user=user or self.business_user,
            title=title,
            description=description,
        )

        basic_detail = OfferDetail.objects.create(
            offer=offer,
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

        standard_detail = OfferDetail.objects.create(
            offer=offer,
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

        premium_detail = OfferDetail.objects.create(
            offer=offer,
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

        return (
            offer,
            basic_detail,
            standard_detail,
            premium_detail,
        )

    def get_valid_offer_data(self):
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


class OffersEndpointTestBase(OffersTestBase):

    def setUp(self):
        super().setUp()

        (
            self.offer,
            self.basic_detail,
            self.standard_detail,
            self.premium_detail,
        ) = self.create_offer_with_details()
