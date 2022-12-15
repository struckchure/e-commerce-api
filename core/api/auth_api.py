from rest_framework import status
from rest_framework.response import Response

from core.services.auth_service import AuthService
from e_commerce.decorators import handle_errors
from e_commerce.permissions import IsAuthenticated
from e_commerce.utils import BaseView

auth_service = AuthService()


class RegisterAPI(BaseView):
    @handle_errors()
    def post(self, request):
        return Response(
            {
                "data": auth_service.register_user(
                    first_name=request.data.get("first_name"),
                    last_name=request.data.get("last_name"),
                    username=request.data.get("username"),
                    email=request.data.get("email"),
                    password=request.data.get("password"),
                )
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPI(BaseView):
    @handle_errors()
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        return Response(
            {"data": auth_service.login_user(username=username, password=password)},
            status=status.HTTP_200_OK,
        )


class ProfileAPI(BaseView):

    permission_classes = [
        IsAuthenticated,
    ]

    @handle_errors()
    def get(self, request):
        return Response(
            {"data": auth_service.get_user(user_id=request.user.id)},
            status=status.HTTP_200_OK,
        )
