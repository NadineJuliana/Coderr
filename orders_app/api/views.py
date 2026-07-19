from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.models import Order

from .permissions import (
    IsCustomerForCreate,
    IsOrderBusinessUserForUpdate,
    IsStaffForDelete,
)
from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
)


User = get_user_model()

# Create your views here.


class OrderListCreateView(ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        user = self.request.user

        return Order.objects.filter(
            Q(customer_user=user)
            | Q(business_user=user)
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer

        return OrderSerializer

    def get_permissions(self):
        permissions = [
            IsAuthenticated(),
        ]

        if self.request.method == "POST":
            permissions.append(
                IsCustomerForCreate(),
            )

        return permissions


class OrderDetailView(
    RetrieveUpdateDestroyAPIView
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_permissions(self):
        permissions = [
            IsAuthenticated(),
        ]

        if self.request.method == "PATCH":
            permissions.append(
                IsOrderBusinessUserForUpdate(),
            )

        if self.request.method == "DELETE":
            permissions.append(
                IsStaffForDelete(),
            )

        return permissions


class OrderCountView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        business_user_id,
    ):
        get_object_or_404(
            User,
            id=business_user_id,
            type="business",
        )

        order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.OrderStatus.IN_PROGRESS,
        ).count()

        return Response(
            {
                "order_count": order_count,
            }
        )


class CompletedOrderCountView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        business_user_id,
    ):
        get_object_or_404(
            User,
            id=business_user_id,
            type="business",
        )

        completed_order_count = Order.objects.filter(
            business_user_id=business_user_id,
            status=Order.OrderStatus.COMPLETED,
        ).count()

        return Response(
            {
                "completed_order_count": (
                    completed_order_count
                ),
            }
        )
