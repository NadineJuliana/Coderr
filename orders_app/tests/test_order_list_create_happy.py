"""
Tests for successful order list and creation requests.
"""

from django.urls import reverse
from rest_framework import status

from orders_app.models import Order
from orders_app.tests.base import OrdersEndpointTestBase


class OrderListCreateAPITestCaseHappy(
    OrdersEndpointTestBase
):
    """
    Tests successful order listing and creation.
    """

    def test_customer_can_get_own_orders(self):
        """
        Tests that a customer receives only their own orders.
        """

        self.create_order(
            customer_user=self.other_customer_user,
            title="Foreign Customer Order",
        )

        self.authenticate(
            self.customer_token,
        )

        url = reverse("order-list")

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
            self.order.id,
        )
        self.assertEqual(
            response.data[0]["customer_user"],
            self.customer_user.id,
        )
        self.assertEqual(
            response.data[0]["business_user"],
            self.business_user.id,
        )
        self.assertEqual(
            response.data[0]["title"],
            self.order.title,
        )
        self.assertEqual(
            response.data[0]["status"],
            Order.OrderStatus.IN_PROGRESS,
        )

    def test_business_user_can_get_received_orders(self):
        """
        Tests that a business user receives assigned orders.
        """

        self.create_order(
            business_user=self.other_business_user,
            title="Foreign Business Order",
        )

        self.authenticate(
            self.business_token,
        )

        url = reverse("order-list")

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
            self.order.id,
        )

    def test_customer_can_create_order(self):
        """
        Tests that a customer can create an order.
        """

        self.authenticate(
            self.customer_token,
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
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Order.objects.count(),
            2,
        )
        self.assertEqual(
            response.data["customer_user"],
            self.customer_user.id,
        )
        self.assertEqual(
            response.data["business_user"],
            self.business_user.id,
        )
        self.assertEqual(
            response.data["title"],
            self.offer_detail.title,
        )
        self.assertEqual(
            response.data["revisions"],
            self.offer_detail.revisions,
        )
        self.assertEqual(
            response.data["delivery_time_in_days"],
            self.offer_detail.delivery_time_in_days,
        )
        self.assertEqual(
            response.data["price"],
            self.offer_detail.price,
        )
        self.assertEqual(
            response.data["features"],
            self.offer_detail.features,
        )
        self.assertEqual(
            response.data["offer_type"],
            self.offer_detail.offer_type,
        )
        self.assertEqual(
            response.data["status"],
            Order.OrderStatus.IN_PROGRESS,
        )
