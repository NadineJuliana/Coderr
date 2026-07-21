from django.urls import reverse
from rest_framework import status

from orders_app.tests.base import OrdersTestBase


class OrderCountsAPITestCaseUnhappy(OrdersTestBase):

    def test_unauthenticated_user_cannot_get_order_count(
        self,
    ):
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
