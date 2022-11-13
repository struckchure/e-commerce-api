from django.db import models


class TagManager(models.Manager):
    def create(self, **kwargs):
        kwargs["type"] = self.model.META_TYPES.TAG
        return super().create(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.META_TYPES.TAG)


class CategoryManager(models.Manager):
    def create(self, **kwargs):
        kwargs["type"] = self.model.META_TYPES.CATEGORY
        return super().create(**kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(type=self.model.META_TYPES.CATEGORY)


class ProductManager(models.Manager):
    def create(self, **kwargs):
        tags = kwargs.pop("tags", [])

        product = super().create(**kwargs)
        product.tags.add(*tags)

        return product

    def get_queryset(self):
        return super().get_queryset()
