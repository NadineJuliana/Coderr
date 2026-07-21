"""
Shared test setup and helpers for order endpoint tests.
"""

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order

User = get_user_model()


class OrdersTestBase(APITestCase):
    """
    Provides shared users, tokens, and order helper methods.
    """

    def setUp(self):
        """
        Creates customer, business, and staff users with tokens.
        """

        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.other_customer_user = User.objects.create_user(
            username="other_customer_user",
            email="other_customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.other_business_user = User.objects.create_user(
            username="other_business_user",
            email="other_business@mail.de",
            password="examplePassword",
            type="business",
        )

        self.admin_user = User.objects.create_user(
            username="admin_user",
            email="admin@mail.de",
            password="examplePassword",
            type="business",
            is_staff=True,
        )

        self.customer_token = Token.objects.create(
            user=self.customer_user,
        )

        self.other_customer_token = Token.objects.create(
            user=self.other_customer_user,
        )

        self.business_token = Token.objects.create(
            user=self.business_user,
        )

        self.other_business_token = Token.objects.create(
            user=self.other_business_user,
        )

        self.admin_token = Token.objects.create(
            user=self.admin_user,
        )

    def authenticate(self, token):
        """
        Authenticates the test client with the provided token.
        """

        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key,
        )

    def create_order(
        self,
        *,
        customer_user=None,
        business_user=None,
        status_value=Order.OrderStatus.IN_PROGRESS,
        title="Test Order",
    ):
        """
        Creates an order with optional user and status values.
        """

        return Order.objects.create(
            customer_user=customer_user or self.customer_user,
            business_user=business_user or self.business_user,
            title=title,
            revisions=2,
            delivery_time_in_days=7,
            price=200,
            features=["Test Feature"],
            offer_type="standard",
            status=status_value,
        )


class OrdersEndpointTestBase(OrdersTestBase):
    """
    Provides an offer detail and an existing order.
    """

    def setUp(self):
        """
        Creates shared users, an offer detail, and an order.
        """

        super().setUp()

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Logo Design",
            description="Professionelles Logo Design",
        )

        self.offer_detail = OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=[
                "Logo Design",
                "Visitenkarten",
            ],
            offer_type="basic",
        )

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_detail.title,
            revisions=self.offer_detail.revisions,
            delivery_time_in_days=(
                self.offer_detail.delivery_time_in_days
            ),
            price=self.offer_detail.price,
            features=self.offer_detail.features,
            offer_type=self.offer_detail.offer_type,
        )
