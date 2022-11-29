from rest_framework import serializers
from core.models.payment_model import PaymentPlatform, Transaction


class PaymentPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPlatform
        fields = [
            "id",
            "name",
            "platform",
            "active",
            "credentials",
            "added_by",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "credentials": {"write_only": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["added_by"] = (
            instance.added_by.username if instance.added_by else "Deleted User"
        )

        return data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "description",
            "amount",
            "status",
            "type",
            "reference",
            "platform_reference",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "platform_reference": {
                "write_only": True,
                "allow_blank": True,
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["user"] = instance.user.username if instance.user else "Deleted User"

        return data
