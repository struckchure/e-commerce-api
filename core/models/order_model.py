from django.contrib.auth import get_user_model
from django.db import models

from core.models.payment_model import Transaction
from core.models.product_model import Product
from e_commerce.utils import BaseModel, generate_reference

User = get_user_model()


class Order(BaseModel):
    class ORDER_STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    reference = models.CharField(max_length=50, default=generate_reference)
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=50, choices=ORDER_STATUS.choices, default=ORDER_STATUS.PENDING
    )

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Order {self.reference}"

    @property
    def price(self):
        if not self.product:
            return 0
        return self.product.price * self.quantity

    @property
    def payment_status(self):
        if not self.transaction:
            return self.ORDER_STATUS.PENDING
        return self.transaction.status
