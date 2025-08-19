from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class CurrencyChoices(models.TextChoices):
    UAH = "UAH", "UAH"
    USD = "USD", "USD"
    EUR = "EUR", "EUR"

class AddressType(models.TextChoices):
    SHIPPING = "shipping", "Shipping"
    BILLING = "billing", "Billing"

class SellerStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"

class OrderStatus(models.TextChoices):
    CREATED = "created", "Created"
    PAID = "paid", "Paid"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"
    REFUNDED = "refunded", "Refunded"

class PaymentStatus(models.TextChoices):
    REQUIRES_ACTION = "requires_action", "Requires Action"
    SUCCEEDED = "succeeded", "Succeeded"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"

class ShipmentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SHIPPED = "shipped", "Shipped"
    IN_TRANSIT = "in_transit", "In transit"
    DELIVERED = "delivered", "Delivered"
    RETURNED = "returned", "Returned"

class PayoutStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
