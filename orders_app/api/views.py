"""
Views for listing, creating, updating, and deleting orders.
"""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
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
    """
    Lists user-related orders and allows customers to create orders.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        """
        Returns orders belonging to the authenticated user.
        """

        user = self.request.user

        return Order.objects.filter(
            Q(customer_user=user)
            | Q(business_user=user)
        )

    def get_serializer_class(self):
        """
        Returns the serializer matching the request method.
        """

        if self.request.method == "POST":
            return OrderCreateSerializer

        return OrderSerializer

    def get_permissions(self):
        """
        Adds the customer permission to order creation requests.
        """

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
    """
    Retrieves orders and controls update and deletion permissions.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_permissions(self):
        """
        Returns permissions matching the request method.
        """

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
    """
    Returns the active order count for a business user.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        business_user_id,
    ):
        """
        Returns the number of orders currently in progress.
        """

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
    """
    Returns the completed order count for a business user.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        business_user_id,
    ):
        """
        Returns the number of completed orders.
        """

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
