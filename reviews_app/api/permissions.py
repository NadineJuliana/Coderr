"""
Permissions for creating and modifying reviews.
"""

from rest_framework.permissions import BasePermission


class IsCustomerForCreate(BasePermission):
    """
    Allows only customer users to create reviews.
    """

    message = (
        "Only customer users can create reviews."
    )

    def has_permission(
        self,
        request,
        view,
    ):
        """
        Checks whether the requesting user is an authenticated customer.
        """

        return (
            request.user.is_authenticated
            and request.user.type == "customer"
        )


class IsReviewAuthor(BasePermission):
    """
    Allows only the review author to modify a review.
    """

    message = (
        "Only the author can modify this review."
    )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        """
        Checks whether the requesting user authored the review.
        """

        return obj.reviewer == request.user
