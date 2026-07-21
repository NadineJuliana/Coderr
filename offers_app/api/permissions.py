"""
Permissions for creating and modifying offers.
"""

from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)


class IsBusinessUser(BasePermission):
    """
    Allows only authenticated business users.
    """

    def has_permission(self, request, view):
        """
        Checks whether the requesting user is a business user.
        """

        return (
            request.user.is_authenticated
            and request.user.type == "business"
        )


class IsOfferOwnerOrReadOnly(BasePermission):
    """
    Allows read access and restricts changes to the offer owner.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        """
        Checks whether the user may access or modify the offer.
        """

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
