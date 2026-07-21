"""
Tests for unsuccessful order count endpoint requests.
"""

from django.urls import reverse
from rest_framework import status

from orders_app.tests.base import OrdersTestBase


class OrderCountsAPITestCaseUnhappy(OrdersTestBase):
    """
    Tests authentication and invalid user errors.
    """

    def test_unauthenticated_user_cannot_get_order_count(
        self,
    ):
        """
        Tests that unauthenticated count requests return 401.
        """

        url = reverse(
            "order-count",
            kwargs={
                "business_user_id": self.business_user.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_order_count_returns_404_for_missing_business_user(
        self,
    ):
        """
        Tests that a missing business user returns 404.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "order-count",
            kwargs={
                "business_user_id": 9999,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_order_count_returns_404_for_customer_id(
        self,
    ):
        """
        Tests that a customer ID returns 404.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "order-count",
            kwargs={
                "business_user_id": self.customer_user.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_get_completed_count(
        self,
    ):
        """
        Tests that unauthenticated completed counts return 401.
        """

        url = reverse(
            "completed-order-count",
            kwargs={
                "business_user_id": self.business_user.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_completed_count_returns_404_for_missing_business_user(
        self,
    ):
        """
        Tests that a missing user returns 404 for completed counts.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "completed-order-count",
            kwargs={
                "business_user_id": 9999,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_completed_count_returns_404_for_customer_id(
        self,
    ):
        """
        Tests that a customer ID returns 404 for completed counts.
        """

        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "completed-order-count",
            kwargs={
                "business_user_id": self.customer_user.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
