"""
Permissions for reading and updating user profiles.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsProfileOwnerOrReadOnly(BasePermission):
    """
    Allows profile updates only for the profile owner.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        """
        Allows safe requests and restricts changes to the owner.
        """

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
