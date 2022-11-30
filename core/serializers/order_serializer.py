from rest_framework import serializers
from core.models.order_model import Order


class OrderSerializer(serializers.ModelSerializer):

    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_payment_status(self, obj):
        return obj.payment_status
