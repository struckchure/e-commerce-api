import uuid

from django.db import models
from rest_framework.generics import GenericAPIView


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
