from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction
from .models import Cart, CartItem
from catalog.models import Product
from catalog.forms import AddToCartForm
from .services import add_item, update_item


def _get_or_create_cart(request) -> Cart:
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    user = request.user if request.user.is_authenticated else None
    cart, _ = Cart.objects.get_or_create(user=user, session_key=session_key)
    return cart


def cart_detail(request):
    cart = _get_or_create_cart(request)
    items = cart.items.select_related(
        "product",
        "product__seller"
    ).all()
    groups = {}
    for it in items:
        key = it.product.seller
        groups.setdefault(key, []).append(it)
    return render(
        request,
        "cart/detail.html",
        {"cart": cart, "groups": groups}
    )


@require_POST
@transaction.atomic
def cart_add(request):
    form = AddToCartForm(request.POST)
    if form.is_valid():
        cart = _get_or_create_cart(request)
        product = get_object_or_404(Product, pk=form.cleaned_data["product_id"])
        add_item(cart, product, form.cleaned_data["quantity"])
        messages.success(request, "Product added to cart")
    return redirect(request.POST.get("next") or "cart_detail")


@require_POST
@transaction.atomic
def cart_update(request, item_id: int):
    cart = _get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    try:
        qty = int(request.POST.get("quantity", 1))
    except ValueError:
        qty = 1
    update_item(cart, item.product, qty)
    return redirect("cart_detail")
