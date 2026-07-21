"""
Views for retrieving and updating user profiles.
"""

from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from profile_app.models import Profile

from .permissions import IsProfileOwnerOrReadOnly
from .serializers import (
    BusinessProfileSerializer,
    CustomerProfileSerializer,
    ProfileSerializer,
)

# Create your views here.


class ProfileDetailView(RetrieveUpdateAPIView):
    """
    Retrieves profiles and allows owners to update their profile.
    """

    permission_classes = [
        IsAuthenticated,
        IsProfileOwnerOrReadOnly,
    ]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    lookup_field = "user_id"
    lookup_url_kwarg = "pk"


class BusinessProfileListView(ListAPIView):
    """
    Returns a list containing all business profiles.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BusinessProfileSerializer

    def get_queryset(self):
        """
        Returns profiles belonging to business users.
        """

        return Profile.objects.filter(
            user__type="business",
        )


class CustomerProfileListView(ListAPIView):
    """
    Returns a list containing all customer profiles.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        """
        Returns profiles belonging to customer users.
        """

        return Profile.objects.filter(
            user__type="customer",
        )
