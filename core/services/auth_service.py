from core.serializers.auth_serializer import LoginSerializer, UserSerializer
from e_commerce import exceptions
from e_commerce.utils import remove_none_values
from rest_framework.authtoken.models import Token


class AuthService:
    def register_user(
        self,
        first_name=None,
        last_name=None,
        username=None,
        email=None,
        password=None,
    ):
        register_user_serializer = UserSerializer(
            data=remove_none_values(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "username": username,
                    "email": email,
                    "password": password,
                }
            )
        )

        if not register_user_serializer.is_valid():
            raise exceptions.Exception(register_user_serializer.errors)

        register_user_serializer.save()

        token = Token.objects.create(user=register_user_serializer.instance)

        return {**register_user_serializer.data, "token": token.key}

    def login_user(self, username, password):
        login_user_serializer = LoginSerializer(
            data={"username": username, "password": password}
        )

        if not login_user_serializer.is_valid():
            raise exceptions.Exception(login_user_serializer.errors)

        login_user_serializer.save()

        token, _ = Token.objects.get_or_create(user=login_user_serializer.instance)

        return {**login_user_serializer.data, "token": token.key}
