"""
Tests for successful order count endpoint requests.
"""

from django.urls import reverse
from rest_framework import status

from orders_app.models import Order
from orders_app.tests.base import OrdersTestBase


class OrderCountsAPITestCaseHappy(OrdersTestBase):
    """
    Tests successful active and completed order counts.
    """

    def setUp(self):
        """
        Creates shared users and an active order.
        """

        super().setUp()

        self.order = self.create_order(
            title="Logo Design",
        )

    def test_authenticated_user_can_get_in_progress_order_count(
        self,
    ):
        """
        Tests retrieving the active order count.
        """

        self.create_order(
            title="Website Design",
        )

        self.create_order(
            title="Completed Design",
            status_value=Order.OrderStatus.COMPLETED,
        )

        self.create_order(
            business_user=self.other_business_user,
            title="Foreign In Progress Order",
        )

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "order-count",
            kwargs={
                "business_user_id": self.business_user.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["order_count"],
            2,
        )

    def test_authenticated_user_can_get_completed_order_count(
        self,
    ):
        """
        Tests retrieving the completed order count.
        """

        self.create_order(
            title="Completed Logo Design",
            status_value=Order.OrderStatus.COMPLETED,
        )

        self.create_order(
            title="Second Completed Order",
            status_value=Order.OrderStatus.COMPLETED,
        )

        self.create_order(
            business_user=self.other_business_user,
            title="Foreign Completed Order",
            status_value=Order.OrderStatus.COMPLETED,
        )

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "completed-order-count",
            kwargs={
                "business_user_id": self.business_user.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["completed_order_count"],
            2,
        )
