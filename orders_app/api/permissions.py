"""
Permissions for creating, updating, and deleting orders.
"""

from rest_framework.permissions import BasePermission


class IsCustomerForCreate(BasePermission):
    """
    Allows only authenticated customer users to create orders.
    """

    message = (
        "Only customer users can create orders."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        """
        Checks whether the requesting user is a customer.
        """

        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )


class IsOrderBusinessUserForUpdate(BasePermission):
    """
    Allows only the assigned business user to update an order.
    """

    message = (
        "Only the assigned business user "
        "can update this order."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        """
        Checks whether the requesting user is a business user.
        """

        return (
            request.user.is_authenticated
            and request.user.type == "business"
        )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        """
        Checks whether the business user is assigned to the order.
        """

        return obj.business_user == request.user


class IsStaffForDelete(BasePermission):
    """
    Allows only authenticated staff users to delete orders.
    """

    message = (
        "Only staff users can delete orders."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        """
        Checks whether the requesting user is a staff member.
        """

        return (
            request.user.is_authenticated
            and request.user.is_staff
        )
