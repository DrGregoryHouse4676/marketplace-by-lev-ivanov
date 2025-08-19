from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST, csrf_exempt
from django.http import HttpResponse
import stripe
from .models import Payment
from .services import mark_payment_succeeded
from orders.models import Order
from payouts.services import create_payout_for_order

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", None)


@require_POST
def start_payment(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id, buyer=request.user)
    payment = Payment.objects.create(
        order=order,
        provider="stripe",
        provider_charge_id=f"pending_{order.id}",
        amount=order.total,
        currency=order.currency,
    )
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": order.currency.lower(),
                "product_data": {"name": f"Order #{order.id}"},
                "unit_amount": int(order.total * 100),
            },
            "quantity": 1,
        }],
        metadata={"order_id": str(order.id)},
        success_url=f"{settings.SITE_URL}/"
                    f"payments/success/?order_id={order.id}",
        cancel_url=f"{settings.SITE_URL}/orders/created/",
    )
    return redirect(session.url)


def payment_success(request):
    # Payment status is finally confirmed by webhook
    return redirect("orders_created")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            endpoint_secret
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        sess = event["data"]["object"]
        order_id = int(sess.get("metadata", {}).get("order_id", 0))
        if order_id:
            try:
                payment = (Payment.objects.select_related("order").
                           get(order_id=order_id))
            except Payment.DoesNotExist:
                return HttpResponse(status=200)
            intent_id = sess.get("payment_intent")
            mark_payment_succeeded(payment, provider_charge_id=intent_id)
            # create a payout in pending status (manual)
            create_payout_for_order(payment.order)
    return HttpResponse(status=200)
