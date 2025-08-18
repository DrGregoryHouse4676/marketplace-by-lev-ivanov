from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .services import checkout_cart
from cart.views import _get_or_create_cart
from .models import Order, Shipment
from .forms import CheckoutForm
from core.models import ShipmentStatus


@login_required
@transaction.atomic
def checkout(request):
    cart = _get_or_create_cart(request)
    if request.method == "POST":
        form = CheckoutForm(
            request.POST,
            user=request.user
        )
        if form.is_valid():
            try:
                orders = checkout_cart(
                    cart,
                    request.user,
                    form.cleaned_data["shipping_address"]
                )
            except ValueError as e:
                messages.error(request, str(e))
                return redirect("cart_detail")
            if not orders:
                messages.info(request, "Cart is empty.")
                return redirect("cart_detail")
            request.session["created_order_ids"] = [o.id for o in orders]
            return redirect("orders_created")
    else:
        form = CheckoutForm(user=request.user)
    return render(
        request,
        "orders/checkout.html",
        {"form": form}
    )


def orders_created(request):
    ids = request.session.get("created_order_ids", [])
    orders = Order.objects.filter(id__in=ids)
    return render(
        request,
        "orders/created.html",
        {"orders": orders}
    )


# Seller: change delivery status + tracking
@login_required
def seller_shipments(request):
    sp = getattr(request.user, "seller_profile", None)
    if not sp:
        return redirect("seller_status")
    orders = (Order.objects.filter(seller=sp)
              .select_related("shipment").
              order_by("-placed_at")
              )
    return render(
        request,
        "orders/seller_shipments.html",
        {"orders": orders}
    )


@login_required
def set_tracking(request, order_id: int):
    sp = getattr(request.user, "seller_profile", None)
    if not sp:
        return redirect("seller_status")
    order = Order.objects.filter(id=order_id, seller=sp).first()
    if not order:
        return redirect("seller_shipments")
    if request.method == "POST":
        carrier = request.POST.get("carrier", "").strip()
        tracking = request.POST.get("tracking", "").strip()
        shipment, _ = Shipment.objects.get_or_create(order=order)
        shipment.carrier = carrier
        shipment.tracking_number = tracking
        shipment.status = ShipmentStatus.SHIPPED
        shipment.save()
        messages.success(request, "Shipment updated")
        return redirect("seller_shipments")
    return render(
        request,
        "orders/set_tracking.html", {"order": order})
