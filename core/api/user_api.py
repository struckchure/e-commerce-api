from e_commerce.permissions import IsStaff
from e_commerce.utils import BaseView
from e_commerce.decorators import handle_errors
from rest_framework.response import Response
from rest_framework import status
from core.services.user_service import UserService


class ListCreateUserAPI(BaseView):

    permission_classes = [
        IsStaff,
    ]

    @handle_errors()
    def post(self, request):
        user = UserService.create_user(request.data)

        return Response({"data": user}, status=status.HTTP_201_CREATED)

    @handle_errors()
    def get(self, request):
        search = request.query_params.get("search")
        is_staff = request.query_params.get("is_staff")
        skip = request.query_params.get("skip")
        limit = request.query_params.get("limit")

        users = UserService.list_users(search, is_staff, skip, limit)

        return Response({"data": users}, status=status.HTTP_200_OK)


class ChangeStaffStatusAPI(BaseView):

    permission_classes = [
        IsStaff,
    ]

    @handle_errors()
    def put(self, request, user_id):
        is_staff = request.data.get("is_staff")

        user = UserService.change_staff_status(user_id, is_staff)

        return Response({"data": user}, status=status.HTTP_202_ACCEPTED)


class GetUpdateDeleteUserAPI(BaseView):

    permission_classes = [
        IsStaff,
    ]

    @handle_errors()
    def get(self, request, user_id):
        user = UserService.get_user(user_id)

        return Response({"data": user}, status=status.HTTP_200_OK)

    @handle_errors()
    def put(self, request, user_id):
        user = UserService.update_user(user_id, request.data)

        return Response({"data": user}, status=status.HTTP_202_ACCEPTED)

    @handle_errors()
    def delete(self, request, user_id):
        UserService.delete_user(user_id)

        return Response(status=status.HTTP_204_NO_CONTENT)
