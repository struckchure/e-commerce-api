from rest_framework import serializers

from core.models.order_model import Order
from core.services.product_service import ProductService


class OrderSerializer(serializers.ModelSerializer):

    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_payment_status(self, obj):
        return obj.payment_status

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["product"] = ProductService().get_product(data["product"])

        return data
