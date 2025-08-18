from .models import Payment
from core.models import PaymentStatus


def mark_payment_succeeded(
        payment: Payment,
        provider_charge_id: str
) -> Payment:
    payment.provider_charge_id = provider_charge_id
    payment.status = PaymentStatus.SUCCEEDED
    payment.save(update_fields=["provider_charge_id", "status", "updated_at"])
    return payment
