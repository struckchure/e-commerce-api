import secrets
import uuid

import requests
from django.conf import settings
from django.db import models
from rest_framework import status
from rest_framework.generics import GenericAPIView

from e_commerce import exceptions
from e_commerce.decorators import raise_errors


class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseView(GenericAPIView):
    pass


def remove_none_values(obj):
    """Remove none values from dict/list"""

    if isinstance(obj, dict):
        return {k: remove_none_values(v) for k, v in obj.items() if v is not None}
    elif isinstance(obj, list):
        return [remove_none_values(v) for v in obj if v is not None]
    else:
        return obj


def get_object_or_error(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise exceptions.Exception(
            "%s does not exist" % model.__name__, code=status.HTTP_404_NOT_FOUND
        )
    except model.MultipleObjectsReturned:
        raise exceptions.Exception(
            "%s has multiple objects" % model.__name__,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except exceptions.Exception as error:
        raise error


def get_or_create(model, **kwargs):
    object = model.objects.filter(**kwargs).first()
    if object:
        return object
    return model.objects.create(**kwargs)


class FileStorageAPI:

    base_url = settings.FILE_STORAGE_URL

    @raise_errors()
    def _upload_file(self, file):
        return requests.post(
            "%s/files/" % self.base_url,
            files={"file": file},
        ).json()["file"]

    @raise_errors()
    def upload_file(self, *files):
        return list(map(self._upload_file, files))


def generate_reference():
    return secrets.token_hex(8).upper()
