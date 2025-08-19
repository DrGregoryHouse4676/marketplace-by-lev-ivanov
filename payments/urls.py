from django.urls import path
from .views import start_payment, payment_success, stripe_webhook


urlpatterns = [
    path(
        "payments/start/<int:order_id>/",
        start_payment,
        name="start_payment"
    ),
    path(
        "payments/success/",
        payment_success,
        name="payment_success"
    ),
    path(
        "payments/stripe/webhook/",
        stripe_webhook,
        name="stripe_webhook"
    ),
]
