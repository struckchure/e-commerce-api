from rest_framework import serializers

from core.models.cart_model import CartItem


class CartItemSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "user",
            "product",
            "quantity",
            "price",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "product": {"required": True},
            "quantity": {"required": True, "min_value": 1},
        }

    def get_price(self, obj):
        return obj.price

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["user"] = {
            "id": instance.user.id,
            "username": instance.user.username,
        }
        data["product"] = (
            {
                "id": instance.product.id,
                "name": instance.product.name,
                "price": instance.product.price,
                "images": list(map(lambda x: x.url, instance.product.images)),
            }
            if instance.product
            else None
        )

        return data

    def create(self, validated_data):
        product = validated_data.get("product")
        product_exists_in_cart = CartItem.objects.filter(
            product__id=product.id
        ).exists()

        if product_exists_in_cart:
            product = CartItem.objects.filter(product__id=product.id).first()
            product.quantity += 1
            product.save()

            return product

        return super().create(validated_data)
