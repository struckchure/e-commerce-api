from core.models.cart_model import CartItem
from core.serializers.cart_serializer import CartItemSerializer
from e_commerce import exceptions
from e_commerce.utils import get_object_or_error, remove_none_values


class CartService:
    def list_items(self, user_id, skip=0, limit=10):
        items = CartItem.objects.filter(user_id=user_id)[skip:limit]

        return CartItemSerializer(items, many=True).data

    def get_item(self, item_id):
        item = get_object_or_error(CartItem, id=item_id)

        return CartItemSerializer(item).data

    def add_item(self, user_id, product_id, quantity):
        item_serializer = CartItemSerializer(
            data=remove_none_values(
                {"user": user_id, "product": product_id, "quantity": quantity}
            )
        )

        if not item_serializer.is_valid():
            raise exceptions.Exception(item_serializer.errors)
        item_serializer.save()

        return item_serializer.data

    def update_item(self, item_id, quantity):
        item = get_object_or_error(CartItem, id=item_id)
        item_serializer = CartItemSerializer(
            item, data={"quantity": quantity}, partial=True
        )

        if not item_serializer.is_valid():
            raise exceptions.Exception(item_serializer.errors)
        item_serializer.save()

        return item_serializer.data

    def delete_item(self, item_id):
        item = get_object_or_error(CartItem, id=item_id)
        item.delete()

        return None
