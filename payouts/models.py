from django.db import models
from core.models import TimeStampedModel, PayoutStatus, CurrencyChoices
from accounts.models import SellerProfile
from orders.models import Order


class SellerPayout(TimeStampedModel):
    seller = models.ForeignKey(
        SellerProfile,
        on_delete=models.CASCADE,
        related_name="payouts"
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.PROTECT,
        related_name="payout"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices
    )
    status = models.CharField(
        max_length=12,
        choices=PayoutStatus.choices,
        default=PayoutStatus.PENDING
    )
    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        indexes = [models.Index(fields=["seller", "status"]) ]

