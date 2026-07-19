from rest_framework.permissions import BasePermission


class IsCustomerForCreate(BasePermission):
    message = (
        "Only customer users can create reviews."
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


class IsReviewAuthor(BasePermission):
    message = (
        "Only the author can modify this review."
    )

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        return obj.reviewer == request.user
