from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "provider",
        "provider_charge_id",
        "amount",
        "currency",
        "status"
    )
    list_filter = ("provider", "status")
