from django.conf import settings
from django.db import models
from core.models import TimeStampedModel, AddressType, SellerStatus

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=32, blank=True, null=True)
    default_shipping_address = models.ForeignKey(
        "accounts.Address", on_delete=models.SET_NULL, blank=True, null=True, related_name="default_for_users"
    )
    def __str__(self):
        return f"Profile<{self.user_id}>"

class SellerProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller_profile")
    status = models.CharField(max_length=16, choices=SellerStatus.choices, default=SellerStatus.PENDING)
    display_name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    class Meta:
        indexes = [models.Index(fields=["status"])]
    def __str__(self):
        return f"Seller<{self.display_name}#{self.id}>"

class Address(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    type = models.CharField(max_length=16, choices=AddressType.choices, default=AddressType.SHIPPING)
    is_default = models.BooleanField(default=False)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=2)
    class Meta:
        indexes = [models.Index(fields=["user", "type", "is_default"]) ]
    def __str__(self):
        return f"{self.line1}, {self.city} ({self.country})"
