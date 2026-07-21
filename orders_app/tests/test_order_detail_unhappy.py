"""
Tests for unsuccessful order detail endpoint requests.
"""

from django.urls import reverse
from rest_framework import status

from orders_app.models import Order
from orders_app.tests.base import OrdersEndpointTestBase


class OrderDetailAPITestCaseUnhappy(
    OrdersEndpointTestBase
):
    """
    Tests authentication, permissions, and update validation.
    """

    def get_order_detail_url(self, order_id=None):
        """
        Returns the detail URL for the provided order ID.
        """

        return reverse(
            "order-detail",
            kwargs={
                "pk": order_id or self.order.id,
            },
        )

    def test_unauthenticated_user_cannot_update_order(self):
        """
        Tests that unauthenticated updates return 401.
        """

        data = {
            "status": Order.OrderStatus.COMPLETED,
        }

        response = self.client.patch(
            self.get_order_detail_url(),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.OrderStatus.IN_PROGRESS,
        )

    def test_customer_cannot_update_order(self):
        """
        Tests that a customer cannot update an order.
        """

        self.authenticate(
            self.customer_token,
        )

        data = {
            "status": Order.OrderStatus.COMPLETED,
        }

        response = self.client.patch(
            self.get_order_detail_url(),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.OrderStatus.IN_PROGRESS,
        )

    def test_unassigned_business_user_cannot_update_order(
        self,
    ):
        """
        Tests that an unassigned business user cannot update.
        """

        self.authenticate(
            self.other_business_token,
        )

        data = {
            "status": Order.OrderStatus.COMPLETED,
        }

        response = self.client.patch(
            self.get_order_detail_url(),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.OrderStatus.IN_PROGRESS,
        )

    def test_update_order_rejects_invalid_status(self):
        """
        Tests that an unsupported status returns 400.
        """

        self.authenticate(
            self.business_token,
        )

        data = {
            "status": "finished",
        }

        response = self.client.patch(
            self.get_order_detail_url(),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn(
            "status",
            response.data,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.OrderStatus.IN_PROGRESS,
        )

    def test_update_order_rejects_disallowed_fields(self):
        """
        Tests that fields other than status cannot be updated.
        """

        self.authenticate(
            self.business_token,
        )

        data = {
            "status": Order.OrderStatus.COMPLETED,
            "title": "Changed title",
        }

        response = self.client.patch(
            self.get_order_detail_url(),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.title,
            self.offer_detail.title,
        )
        self.assertEqual(
            self.order.status,
            Order.OrderStatus.IN_PROGRESS,
        )

    def test_update_returns_404_for_missing_order(self):
        """
        Tests that updating a missing order returns 404.
        """

        self.authenticate(
            self.business_token,
        )

        data = {
            "status": Order.OrderStatus.COMPLETED,
        }

        response = self.client.patch(
            self.get_order_detail_url(9999),
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_delete_order(self):
        """
        Tests that unauthenticated deletion returns 401.
        """

        response = self.client.delete(
            self.get_order_detail_url(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertTrue(
            Order.objects.filter(
                id=self.order.id,
            ).exists()
        )

    def test_non_staff_user_cannot_delete_order(self):
        """
        Tests that a non-staff user cannot delete an order.
        """

        self.authenticate(
            self.business_token,
        )

        response = self.client.delete(
            self.get_order_detail_url(),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Order.objects.filter(
                id=self.order.id,
            ).exists()
        )

    def test_admin_gets_404_when_deleting_missing_order(
        self,
    ):
        """
        Tests that deleting a missing order returns 404.
        """

        self.authenticate(
            self.admin_token,
        )

        response = self.client.delete(
            self.get_order_detail_url(9999),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
