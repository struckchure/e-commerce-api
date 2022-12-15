from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers, status

from core.models.auth_model import User
from e_commerce import exceptions


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "is_staff",
            "last_login",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_staff", "last_login", "created_at", "updated_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def create(self, validated_data):
        user = authenticate(**validated_data)

        if not user:
            raise exceptions.Exception(
                message="Invalid username or password",
                code=status.HTTP_401_UNAUTHORIZED,
            )

        user.last_login = timezone.now()
        user.save()

        return user
