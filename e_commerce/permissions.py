from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    message = "You are not authenticated"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    message = "You are not authenticated"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return IsAuthenticated().has_permission(request, view)


class IsStaff(BasePermission):
    """
    Allows access only to staff users.
    """

    message = "You are not authorized to access the resources"

    def has_permission(self, request, view):
        if not request.user:
            return False

        if not request.user.is_staff:
            return False

        return True


class IsStaffOrReadOnly(BasePermission):
    """
    The request is authenticated as a staff, or is a read-only request.
    """

    message = "You are not authorized to access the resources"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return IsStaff().has_permission(request, view)


class IsObjectOwner(BasePermission):
    """
    Allows access only to object owners.
    """

    message = "You are not authorized to access the resources"

    def has_object_permission(self, request, view, user_id):
        if not request.user:
            return False

        return user_id == request.user.id
