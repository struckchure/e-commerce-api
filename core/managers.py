from django.db import models


class TagManager(models.Manager):
    def create(self, **kwargs):
        kwargs["type"] = "TAG"
        return super().create(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(type="TAG")


class CategoryManager(models.Manager):
    def create(self, **kwargs):
        kwargs["type"] = "CATEGORY"
        return super().create(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(type="CATEGORY")
