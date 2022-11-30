from core.models.payment_model import PaymentPlatform, Transaction
from core.serializers.payment_serializer import (
    PaymentPlatformSerializer,
    TransactionSerializer,
)
from django.db import models
from e_commerce.utils import get_object_or_error, remove_none_values
from e_commerce import exceptions


class PaymentPlaformService:
    @staticmethod
    def list_payment_platforms(search=None, skip=0, limit=10):
        payment_platform_list = PaymentPlatform.objects.filter(
            models.Q(name__icontains=search) if search else models.Q(),
        ).distinct()[skip:limit]

        return PaymentPlatformSerializer(payment_platform_list, many=True).data

    @staticmethod
    def get_payment_platform(id):
        payment_platform = get_object_or_error(PaymentPlatform, id=id)

        return PaymentPlatformSerializer(payment_platform).data

    @staticmethod
    def create_payment_platform(
        name,
        platform,
        credentials,
        added_by,
        active=None,
    ):
        payment_platform_create_serializer = PaymentPlatformSerializer(
            data=remove_none_values(
                {
                    "name": name,
                    "platform": platform,
                    "active": active,
                    "credentials": credentials,
                    "added_by": added_by,
                }
            )
        )
        if not payment_platform_create_serializer.is_valid():
            raise exceptions.Exception(payment_platform_create_serializer.errors)

        # deactivate all other payment platforms if this one is active
        if active:
            PaymentPlatform.objects.update(active=False)

        payment_platform_create_serializer.save()

        return payment_platform_create_serializer.data

    @staticmethod
    def update_payment_platform(
        id,
        name=None,
        platform=None,
        active=None,
        credentials=None,
    ):
        payment_platform = get_object_or_error(PaymentPlatform, id=id)

        payment_platform_update_serializer = PaymentPlatformSerializer(
            payment_platform,
            data=remove_none_values(
                {
                    "name": name,
                    "platform": platform,
                    "active": active,
                    "credentials": credentials,
                }
            ),
            partial=True,
        )
        if not payment_platform_update_serializer.is_valid():
            raise exceptions.Exception(payment_platform_update_serializer.errors)

        # deactivate all other payment platforms if this one is active
        if active:
            PaymentPlatform.objects.update(active=False)

        payment_platform_update_serializer.save()

        return payment_platform_update_serializer.data

    @staticmethod
    def delete_payment_platform(id):
        payment_platform = get_object_or_error(PaymentPlatform, id=id)

        payment_platform.delete()


class TransactionService:
    @staticmethod
    def list_transactions(
        search=None, transaction_type=None, transaction_status=None, skip=0, limit=10
    ):
        transaction_list = Transaction.objects.filter(
            models.Q(reference__icontains=search)
            | models.Q(description__icontains=search)
            if search
            else models.Q(),
            models.Q(type=transaction_type) if transaction_type else models.Q(),
            models.Q(status=transaction_status) if transaction_status else models.Q(),
        ).distinct()[skip:limit]

        return TransactionSerializer(transaction_list, many=True).data

    @staticmethod
    def get_transaction(id):
        transaction = get_object_or_error(Transaction, id=id)

        return TransactionSerializer(transaction).data

    @staticmethod
    def create_transaction(
        user, amount, type, description=None, platform_reference=None
    ):
        transaction_create_serializer = TransactionSerializer(
            data=remove_none_values(
                {
                    "user": user,
                    "description": description,
                    "amount": amount,
                    "type": type,
                    "platform_reference": platform_reference,
                }
            )
        )
        if not transaction_create_serializer.is_valid():
            raise exceptions.Exception(transaction_create_serializer.errors)
        transaction_create_serializer.save()

        return transaction_create_serializer.data

    @staticmethod
    def delete_transaction(id):
        transaction = get_object_or_error(Transaction, id=id)

        transaction.delete()


class PaymentService(TransactionService, PaymentPlaformService):
    """
    PaymentService is a class that inherits from;
    - `TransactionService`
    - `PaymentPlaformService`
    """
