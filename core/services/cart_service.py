from django.db import models

from core.models.cart_model import CartItem
from core.serializers.cart_serializer import CartItemSerializer
from core.services.order_service import OrderService
from core.services.platform_payment_service import PaymentService
from e_commerce import exceptions
from e_commerce.utils import get_object_or_error, remove_none_values


class CartService:
    @staticmethod
    def list_items(user_id, skip=0, limit=10):
        items = CartItem.objects.filter(user_id=user_id)[skip:limit]
        cart_total = sum([item.price for item in items])

        return CartItemSerializer(items, many=True).data, cart_total

    @staticmethod
    def get_item(item_id):
        item = get_object_or_error(CartItem, id=item_id)

        return CartItemSerializer(item).data

    @staticmethod
    def add_item(user_id, product_id, quantity):
        item_serializer = CartItemSerializer(
            data=remove_none_values(
                {"user": user_id, "product": product_id, "quantity": quantity}
            )
        )

        if not item_serializer.is_valid():
            raise exceptions.Exception(item_serializer.errors)
        item_serializer.save()

        return item_serializer.data

    @staticmethod
    def update_item(item_id, quantity):
        item = get_object_or_error(CartItem, id=item_id)
        item_serializer = CartItemSerializer(
            item, data={"quantity": quantity}, partial=True
        )

        if not item_serializer.is_valid():
            raise exceptions.Exception(item_serializer.errors)
        item_serializer.save()

        return item_serializer.data

    @staticmethod
    def delete_item(item_id):
        item = get_object_or_error(CartItem, id=item_id)
        item.delete()

        return None

    @staticmethod
    def checkout(user_id, cart_items=None):
        items = CartItem.objects.filter(
            **remove_none_values({"user": user_id, "id__in": cart_items})
        )

        amount = sum(map(lambda item: item.price, items))
        email = items.first().user.email
        payment = PaymentService().initiate_payment(amount, email)

        orders = list(
            map(
                lambda item: OrderService.create_order(
                    user_id=user_id,
                    product=item.product.id,
                    quantity=item.quantity,
                    transaction_id=payment["id"],
                ),
                items,
            )
        )

        if orders:
            items.delete()

        return {
            "url": payment["url"],
            "message": "Orders have been placed. Proceed to payment.",
        }
