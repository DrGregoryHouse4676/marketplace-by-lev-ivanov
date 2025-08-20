from django.db import models
from core.enums import PayoutStatus

class SellerPayout(models.Model):
    seller = models.ForeignKey(
        "accounts.SellerProfile",
        on_delete=models.PROTECT,
        related_name="payouts"
    )
    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="payout"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(
        max_length=20,
        choices=PayoutStatus.choices,
        default=PayoutStatus.PENDING
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
