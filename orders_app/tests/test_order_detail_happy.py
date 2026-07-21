from django.urls import reverse
from rest_framework import status

from orders_app.models import Order
from orders_app.tests.base import OrdersEndpointTestBase


class OrderDetailAPITestCaseHappy(
    OrdersEndpointTestBase
):

    def test_business_user_can_update_order_status(self):
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "order-detail",
            kwargs={
                "pk": self.order.id,
            },
        )

        data = {
            "status": Order.OrderStatus.COMPLETED,
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
            response.data["status"],
            Order.OrderStatus.COMPLETED,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            Order.OrderStatus.COMPLETED,
        )

    def test_admin_can_delete_order(self):
        self.authenticate(
            self.admin_token,
        )

        url = reverse(
            "order-detail",
            kwargs={
                "pk": self.order.id,
            },
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Order.objects.filter(
                id=self.order.id,
            ).exists()
        )
