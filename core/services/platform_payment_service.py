from rest_framework import status
from django.contrib.auth import get_user_model

from core.models.payment_model import PaymentPlatform, Transaction
from core.platforms.paystack import PaystackEvents, Paystack
from core.services.payment_service import TransactionService
from e_commerce import exceptions
from e_commerce.utils import get_object_or_error


User = get_user_model()


class PaystackService:

    paystack_platform = None

    def __init__(self):

        active_payment_platform = PaymentPlatform.objects.filter(
            active=True, platform=PaymentPlatform.AVAILABLE_PLATFORMS.PAYSTACK
        )
        if not active_payment_platform.exists():
            raise exceptions.Exception("Not active paystack credentials")

        credentials = {
            "public_key": active_payment_platform.first().credentials["PUBLIC_KEY"],
            "secret_key": active_payment_platform.first().credentials["SECRET_KEY"],
        }
        self.paystack_platform = Paystack(**credentials)

    def initiate_payment(self, amount, email):
        user = get_object_or_error(User, email=email)

        payment = self.paystack_platform.initiate_payment(amount=amount, email=email)
        platform_reference = payment["data"]["reference"]

        transaction = TransactionService.create_transaction(
            user=user.id,
            amount=amount,
            platform_reference=platform_reference,
            type=Transaction.TRANSACTION_TYPE.DEBIT,
        )

        return {**transaction, "url": payment["data"]["authorization_url"]}

    @staticmethod
    def verify_payment(data):
        event = data["event"]
        reference = data["data"]["reference"]
        transaction = get_object_or_error(Transaction, platform_reference=reference)

        match event:
            case PaystackEvents.SUCCESS.value:
                transaction.status = Transaction.TRANSACTION_STATUS.SUCCESSFUL
                transaction.save()

                return {"message": "Verification successful"}
            case PaystackEvents.FAILED.value:
                transaction.status = Transaction.TRANSACTION_STATUS.FAILED
                transaction.save()

                raise exceptions.Exception(
                    {"message": "Verification failed"}, code=status.HTTP_400_BAD_REQUEST
                )
            case _:
                transaction.status = Transaction.TRANSACTION_STATUS.PENDING
                transaction.save()

                raise exceptions.Exception(
                    {"message": "Could not verify payment"},
                    code=status.HTTP_400_BAD_REQUEST,
                )


class PaymentService:

    platform = PaymentPlatform.objects.filter(active=True).first().platform

    @classmethod
    def initiate_payment(cls, amount, email):
        match cls.platform:
            case PaymentPlatform.AVAILABLE_PLATFORMS.PAYSTACK:
                return PaystackService().initiate_payment(amount=amount, email=email)
            case _:
                raise exceptions.Exception(
                    {"message": "Payment platform not supported"},
                    code=status.HTTP_400_BAD_REQUEST,
                )

    @classmethod
    def verify_payment(cls, data):
        match cls.platform:
            case PaymentPlatform.AVAILABLE_PLATFORMS.PAYSTACK:
                return PaystackService().verify_payment(data=data)
            case _:
                raise exceptions.Exception(
                    {"message": "Payment platform not supported"},
                    code=status.HTTP_400_BAD_REQUEST,
                )
