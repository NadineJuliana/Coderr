from rest_framework.permissions import BasePermission


class IsCustomerForCreate(BasePermission):
    message = (
        "Only customer users can create orders."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )


class IsOrderBusinessUserForUpdate(BasePermission):
    message = (
        "Only the assigned business user "
        "can update this order."
    )

    def has_permission(
        self,
        request,
        view,
    ):
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
        return obj.business_user == request.user


class IsStaffForDelete(BasePermission):
    message = (
        "Only staff users can delete orders."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        return (
            request.user.is_authenticated
            and request.user.is_staff
        )
