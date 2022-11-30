from core.serializers.order_serializer import OrderSerializer
from core.models.order_model import Order
from e_commerce import exceptions
from e_commerce.utils import get_object_or_error, remove_none_values


class OrderService:
    @staticmethod
    def list_orders(user_id=None, skip=0, limit=10):
        orders = Order.objects.filter(**remove_none_values({"user__id": user_id}))[
            skip:limit
        ]

        return OrderSerializer(orders, many=True).data

    @staticmethod
    def create_order(user_id, product, quantity, transaction_id):
        order_serializer = OrderSerializer(
            data=remove_none_values(
                {
                    "user": user_id,
                    "transaction": transaction_id,
                    "product": product,
                    "quantity": quantity,
                }
            )
        )

        if not order_serializer.is_valid():
            raise exceptions.Exception(order_serializer.errors)
        order_serializer.save()

        return order_serializer.data

    @staticmethod
    def get_order(order_id):
        order = get_object_or_error(Order, id=order_id)

        return OrderSerializer(order).data

    @staticmethod
    def update_order(order_id, status):
        order = get_object_or_error(Order, id=order_id)
        order.status = status
        order.save()

        return OrderSerializer(order).data

    @staticmethod
    def delete_order(order_id):
        order = get_object_or_error(Order, id=order_id)
        order.delete()

        return None
