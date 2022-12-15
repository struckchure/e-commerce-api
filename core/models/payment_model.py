from django.contrib.auth import get_user_model
from django.db import models

from e_commerce.utils import BaseModel, generate_reference

User = get_user_model()


class PaymentPlatform(BaseModel):
    class AVAILABLE_PLATFORMS(models.TextChoices):
        PAYSTACK = "PAYSTACK", "Paystack"

    name = models.CharField(max_length=50, unique=True)
    platform = models.CharField(max_length=50, choices=AVAILABLE_PLATFORMS.choices)
    active = models.BooleanField(default=False)
    credentials = models.JSONField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class Wallet(BaseModel):

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    class Meta:
        ordering = ["-created_at"]


class Transaction(BaseModel):
    class TRANSACTION_STATUS(models.TextChoices):
        SUCCESSFUL = "SUCCESSFUL", "Successful"
        PENDING = "PENDING", "Pending"
        FAILED = "FAILED", "Failed"

    class TRANSACTION_TYPE(models.TextChoices):
        DEBIT = "DEBIT", "Debit"
        CREDIT = "CREDIT", "Credit"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=TRANSACTION_STATUS.choices,
        default=TRANSACTION_STATUS.PENDING,
    )
    type = models.CharField(max_length=50, choices=TRANSACTION_TYPE.choices)
    reference = models.CharField(max_length=50, default=generate_reference)
    platform_reference = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Transaction"

    class Meta:
        ordering = ["-created_at"]
