from django.db import models
from core.models import TimeStampedModel, PaymentStatus, CurrencyChoices
from orders.models import Order


class Payment(TimeStampedModel):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )
    provider = models.CharField(max_length=32)  # 'stripe'
    provider_charge_id = models.CharField(
        max_length=128,
        unique=True
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
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.REQUIRES_ACTION
    )

    class Meta:
        indexes = [models.Index(fields=["provider", "status"]) ]