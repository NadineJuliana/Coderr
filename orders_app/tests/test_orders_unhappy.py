from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


User = get_user_model()


class OrdersAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer_user",
            email="customer@mail.de",
            password="examplePassword",
            type="customer",
        )

        self.other_customer = User.objects.create_user(
            username="other_customer",
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
            username="other_business",
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
            user=self.other_customer,
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
            HTTP_AUTHORIZATION=f"Token {token.key}",
        )

    def test_unauthenticated_user_cannot_get_orders(self):
        url = reverse("order-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_cannot_see_unrelated_orders(self):
        self.authenticate(
            self.other_customer_token,
        )

        url = reverse("order-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            0,
        )

    def test_unauthenticated_user_cannot_create_order(self):
        url = reverse("order-list")

        response = self.client.post(
            url,
            {
                "offer_detail_id": self.offer_detail.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_business_user_cannot_create_order(self):
        self.authenticate(
            self.business_token,
        )

        url = reverse("order-list")

        response = self.client.post(
            url,
            {
                "offer_detail_id": self.offer_detail.id,
            },
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

    def test_create_order_returns_404_for_missing_offer_detail(
        self,
    ):
        self.authenticate(
            self.customer_token,
        )

        url = reverse("order-list")

        response = self.client.post(
            url,
            {
                "offer_detail_id": 9999,
            },
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

    def test_unauthenticated_user_cannot_update_order(self):
        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
        )

        response = self.client.patch(
            url,
            {
                "status": Order.OrderStatus.COMPLETED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_customer_cannot_update_order(self):
        self.authenticate(
            self.customer_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
        )

        response = self.client.patch(
            url,
            {
                "status": Order.OrderStatus.COMPLETED,
            },
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
        self.authenticate(
            self.other_business_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
        )

        response = self.client.patch(
            url,
            {
                "status": Order.OrderStatus.COMPLETED,
            },
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
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
        )

        response = self.client.patch(
            url,
            {
                "status": "finished",
            },
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

    def test_update_order_rejects_disallowed_fields(self):
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
        )

        response = self.client.patch(
            url,
            {
                "status": Order.OrderStatus.COMPLETED,
                "title": "Changed title",
            },
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
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": 9999},
        )

        response = self.client.patch(
            url,
            {
                "status": Order.OrderStatus.COMPLETED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_delete_order(self):
        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
        )

        response = self.client.delete(url)

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
        self.authenticate(
            self.business_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": self.order.id},
        )

        response = self.client.delete(url)

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
        self.authenticate(
            self.admin_token,
        )

        url = reverse(
            "order-detail",
            kwargs={"pk": 9999},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

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

    def test_completed_count_returns_404_for_missing_user(
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
