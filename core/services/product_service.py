from django.db import models

from core.models.product_model import Product
from core.serializers.product_serializer import ProductSerializer
from e_commerce import exceptions
from e_commerce.utils import get_object_or_error, remove_none_values


class ProductService:
    @staticmethod
    def list_product(search=None, skip=0, limit=10):
        product_list = Product.objects.filter(
            models.Q(name__icontains=search)
            | models.Q(description__icontains=search)
            | models.Q(category__name__icontains=search)
            | models.Q(tags__name__icontains=search)
            if search
            else models.Q(),
        ).distinct()[skip:limit]

        return ProductSerializer(product_list, many=True).data

    @staticmethod
    def get_product(id):
        product = get_object_or_error(Product, id=id)

        return ProductSerializer(product).data

    @staticmethod
    def create_product(
        name,
        description,
        images,
        price,
        stock,
        user_id,
        category=None,
        tags=None,
    ):
        product_create_serializer = ProductSerializer(
            data=remove_none_values(
                {
                    "name": name,
                    "description": description,
                    "images": images,
                    "price": price,
                    "stock": stock,
                    "category": category,
                    "tags": tags,
                    "added_by": user_id,
                }
            )
        )
        if not product_create_serializer.is_valid():
            raise exceptions.Exception(product_create_serializer.errors)
        product_create_serializer.save()

        return product_create_serializer.data

    @staticmethod
    def update_product(
        id,
        name=None,
        description=None,
        images=None,
        price=None,
        stock=None,
        category=None,
        tags=None,
    ):
        product = get_object_or_error(Product, id=id)
        product_update_serializer = ProductSerializer(
            product,
            data=remove_none_values(
                {
                    "name": name,
                    "description": description,
                    "images": images,
                    "price": price,
                    "stock": stock,
                    "category": category,
                    "tags": tags,
                }
            ),
            partial=True,
        )

        if not product_update_serializer.is_valid():
            raise exceptions.Exception(product_update_serializer.errors)
        product_update_serializer.save()

        return product_update_serializer.data

    @staticmethod
    def delete_product(id):
        product = get_object_or_error(Product, id=id)
        product.delete()

        return None
