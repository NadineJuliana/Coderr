from django.urls import reverse
from rest_framework import status

from orders_app.models import Order
from orders_app.tests.base import OrdersEndpointTestBase


class OrderListCreateAPITestCaseUnhappy(
    OrdersEndpointTestBase
):

    def test_unauthenticated_user_cannot_get_orders(self):
        url = reverse("order-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_create_order(self):
        url = reverse("order-list")

        data = {
            "offer_detail_id": self.offer_detail.id,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            Order.objects.count(),
            1,
        )

    def test_business_user_cannot_create_order(self):
        self.authenticate(
            self.business_token,
        )

        url = reverse("order-list")

        data = {
            "offer_detail_id": self.offer_detail.id,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            Order.objects.count(),
            1,
        )

    def test_create_order_requires_offer_detail_id(self):
        self.authenticate(
            self.customer_token,
        )

        url = reverse("order-list")

        response = self.client.post(
            url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn(
            "offer_detail_id",
            response.data,
        )
        self.assertEqual(
            Order.objects.count(),
            1,
        )

    def test_create_order_returns_404_for_missing_offer_detail(
        self,
    ):
        self.authenticate(
            self.customer_token,
        )

        url = reverse("order-list")

        data = {
            "offer_detail_id": 9999,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            Order.objects.count(),
            1,
        )
