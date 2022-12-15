from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response

from core.services.permission_service import PermissionService
from e_commerce.decorators import handle_errors
from e_commerce.permissions import IsStaff
from e_commerce.utils import BaseView


@method_decorator(
    permission_required(
        ["auth.add_permission", "auth.change_permission"], raise_exception=True
    ),
    name="put",
)
class ListUpdatePermissionAPI(BaseView):

    permission_classes = [
        IsStaff,
    ]

    @handle_errors()
    def get(self, request):
        filter_logged_in_user = int(request.query_params.get("me", 0))

        permissions = PermissionService.list_permissions(
            user_id=request.user.id if filter_logged_in_user else None
        )

        return Response({"data": permissions}, status=status.HTTP_200_OK)

    @handle_errors()
    def put(self, request):
        user_id = request.query_params.get("user_id")
        permission_codenames = request.query_params.getlist("codename")
        update_action = request.query_params.get("update_action")

        permission_update = None

        match update_action:
            case "add":
                permission_update = PermissionService.add_user_permissions(
                    user_id,
                    *permission_codenames,
                )
            case "remove":
                permission_update = PermissionService.remove_user_permissions(
                    user_id,
                    *permission_codenames,
                )
            case _:
                return Response(
                    {"error": "Update action is invalid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response({"data": permission_update}, status=status.HTTP_202_ACCEPTED)
