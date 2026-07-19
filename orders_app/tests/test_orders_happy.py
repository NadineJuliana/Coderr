from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


User = get_user_model()


class OrdersAPITestCaseHappy(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.business_user = User.objects.create_user(
            username="business_user",
            email="business@mail.de",
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

        self.business_token = Token.objects.create(
            user=self.business_user,
        )

        self.admin_token = Token.objects.create(
            user=self.admin_user,
        )

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

    def authenticate(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + token.key,
        )

    def test_customer_can_get_own_orders(self):
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
            150,
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

    def test_business_user_can_update_order_status(self):
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
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
            kwargs={"pk": self.order.id},
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

    def test_authenticated_user_can_get_in_progress_order_count(
        self,
    ):
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Website Design",
            revisions=2,
            delivery_time_in_days=7,
            price=300,
            features=[
                "Website",
            ],
            offer_type="standard",
            status=Order.OrderStatus.IN_PROGRESS,
        )

        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Premium Design",
            revisions=5,
            delivery_time_in_days=10,
            price=500,
            features=[
                "Logo",
                "Website",
            ],
            offer_type="premium",
            status=Order.OrderStatus.COMPLETED,
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
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Completed Logo Design",
            revisions=3,
            delivery_time_in_days=5,
            price=150,
            features=[
                "Logo",
            ],
            offer_type="basic",
            status=Order.OrderStatus.COMPLETED,
        )

        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title="Second Completed Order",
            revisions=5,
            delivery_time_in_days=7,
            price=250,
            features=[
                "Logo",
                "Visitenkarte",
            ],
            offer_type="standard",
            status=Order.OrderStatus.COMPLETED,
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
