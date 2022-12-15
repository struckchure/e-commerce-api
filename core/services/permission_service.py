from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.models.auth_model import User
from core.serializers.permission_serializers import PermissionSerializer
from e_commerce.utils import get_object_or_error


class PermissionService:
    @staticmethod
    def list_permissions(user_id=None):
        if user_id:
            user = get_object_or_error(User, id=user_id)

            return PermissionSerializer(user.user_permissions.all(), many=True).data

        default_models = [Permission]
        app_models = [
            *default_models,
            *list(apps.get_app_config("core").get_models()),
        ]

        permissions = [
            PermissionSerializer(
                Permission.objects.filter(
                    content_type=ContentType.objects.get_for_model(model())
                ),
                many=True,
            ).data
            for model in app_models
        ]

        return permissions

    @staticmethod
    def add_user_permissions(user_id, *codenames):
        permissions = Permission.objects.filter(codename__in=codenames)

        user = get_object_or_error(User, id=user_id)
        user.user_permissions.add(*permissions)

        return PermissionSerializer(user.user_permissions.all(), many=True).data

    @staticmethod
    def remove_user_permissions(user_id, *codenames):
        permissions = Permission.objects.filter(codename__in=codenames)

        user = get_object_or_error(User, id=user_id)
        user.user_permissions.remove(*permissions)

        return PermissionSerializer(user.user_permissions.all(), many=True).data
