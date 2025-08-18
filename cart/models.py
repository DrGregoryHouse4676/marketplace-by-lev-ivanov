from django.conf import settings
from django.db import models
from core.models import TimeStampedModel
from catalog.models import Product

class Cart(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True
    )
    session_key = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        db_index=True
    )
    def __str__(self):
        owner = self.user_id or self.session_key or "anon"
        return f"Cart<{owner}:{self.id}>"

class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    class Meta:
        unique_together = ("cart", "product")

    @property
    def line_total(self):
        return self.quantity * self.price_snapshot
