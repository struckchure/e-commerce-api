from django.contrib.auth import get_user_model
from django.db import models

from core.serializers.auth_serializer import UserSerializer
from e_commerce import exceptions
from e_commerce.utils import get_object_or_error, remove_none_values

User = get_user_model()


class UserService:
    @staticmethod
    def list_users(search=None, is_staff=True, skip=None, limit=None):
        skip = abs(int(skip)) if skip else 0
        limit = abs(int(limit)) if limit else 10

        users = User.objects.filter(
            models.Q(username__icontains=search)
            | models.Q(email__icontains=search)
            | models.Q(first_name__icontains=search)
            | models.Q(last_name__icontains=search)
            if search
            else models.Q(),
            **remove_none_values({"is_staff": is_staff}),
        )[skip:limit]

        return UserSerializer(users, many=True).data

    @staticmethod
    def change_staff_status(user_id, is_staff):
        user = get_object_or_error(User, id=user_id)
        user.is_staff = is_staff
        user.save()

        return UserSerializer(user).data

    @staticmethod
    def get_user(user_id):
        user = get_object_or_error(User, id=user_id)

        return UserSerializer(user).data

    @staticmethod
    def create_user(data):
        user_create_serializer = UserSerializer(data=data)

        if not user_create_serializer.is_valid():
            raise exceptions.Exception(user_create_serializer.errors)
        user_create_serializer.save()

        return user_create_serializer.data

    @staticmethod
    def delete_user(user_id):
        user = get_object_or_error(User, id=user_id)
        user.delete()

    @staticmethod
    def update_user(user_id, data):
        user = get_object_or_error(User, id=user_id)
        user_update_serializer = UserSerializer(user, data=data, partial=True)

        if not user_update_serializer.is_valid():
            raise exceptions.Exception(user_update_serializer.errors)
        user_update_serializer.save()

        return user_update_serializer.data
