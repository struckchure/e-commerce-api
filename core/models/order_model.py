from e_commerce.utils import BaseModel, generate_reference
from django.db import models
from django.contrib.auth import get_user_model
from core.models.product_model import Product

User = get_user_model()


class Order(BaseModel):
    class ORDER_STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    class PAYMENT_STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESSFUL = "SUCCESSFUL", "Successful"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    reference = models.CharField(max_length=50, default=generate_reference)

    def __str__(self):
        return f"Order {self.reference}"

    @property
    def price(self):
        if not self.product:
            return 0
        return self.product.price * self.quantity
