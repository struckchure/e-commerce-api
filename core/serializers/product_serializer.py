from core.models.product_model import Category, Image, Product, Tag
from e_commerce.utils import FileStorageAPI, get_or_create
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):

    images = serializers.ListSerializer(child=serializers.FileField(), required=True)
    category = serializers.CharField(required=False)
    tags = serializers.ListSerializer(
        child=serializers.CharField(),
        required=False,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "images",
            "price",
            "stock",
            "category",
            "tags",
        ]

    def create(self, validated_data):
        images = validated_data.pop("images")
        category = None
        tags = None

        if validated_data.get("category"):
            category = get_or_create(Category, name=validated_data.pop("category"))
            validated_data["category"] = category

        if validated_data.get("tags"):
            tags = list(
                map(
                    lambda tag: get_or_create(Tag, name=tag), validated_data.pop("tags")
                )
            )
            validated_data["tags"] = tags

        product = Product.objects.create(**validated_data)

        Image.objects.bulk_create(
            [
                Image(product_id=product.id, url=image)
                for image in FileStorageAPI().upload_file(*images)
            ]
        )

        return product

    def to_representation(self, instance: Product):
        data = super().to_representation(instance)

        data["images"] = [image.url for image in instance.images]
        data["category"] = instance.category.name if instance.category else None
        data["tags"] = (
            instance.tags.all().values_list("name", flat=True) if instance.tags else []
        )

        return data
