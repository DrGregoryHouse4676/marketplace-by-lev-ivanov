from django.conf import settings
from django.db import models
from django.utils import timezone
from core.models import (TimeStampedModel,
                         OrderStatus,
                         ShipmentStatus,
                         CurrencyChoices
                         )
from accounts.models import Address, SellerProfile
from catalog.models import Product


class Order(TimeStampedModel):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    seller = models.ForeignKey(
        SellerProfile,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    status = models.CharField(
        max_length=16,
        choices=OrderStatus.choices,
        default=OrderStatus.CREATED,
        db_index=True
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    shipping_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.UAH
    )
    shipping_address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    placed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [models.Index(fields=["status", "placed_at"])]

    def __str__(self):
        return f"Order#{self.id} ({self.status})"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    product_title_snapshot = models.CharField(max_length=200)
    price_snapshot = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )


class Shipment(TimeStampedModel):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="shipment"
    )
    carrier = models.CharField(max_length=64)
    tracking_number = models.CharField(max_length=64)
    status = models.CharField(
        max_length=16,
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.PENDING
    )
    shipped_at = models.DateTimeField(
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        blank=True,
        null=True
    )
