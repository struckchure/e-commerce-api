from core.models.auth_model import User
from core.models.product_model import Product
from django.db import models
from e_commerce.utils import BaseModel


class CartItem(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Cart item"
        verbose_name_plural = "Cart items"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def price(self):
        if self.product:
            return self.product.price * self.quantity
        return 0
