from rest_framework import status
from rest_framework.permissions import BasePermission

from e_commerce import exceptions


class IsStaff(BasePermission):
    """
    Allows access only to staff users.
    """

    def has_permission(self, request, view):
        if not request.user:
            return False

        if not request.user.is_staff:
            raise exceptions.Exception(
                "You are not authorized to access the resources",
                code=status.HTTP_403_FORBIDDEN,
            )

        return True
