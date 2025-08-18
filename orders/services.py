from collections import defaultdict
from decimal import Decimal
from typing import Dict, List
from django.db import transaction
from django.db.models import F
from accounts.models import Address
from cart.models import Cart, CartItem
from catalog.models import Product
from .models import Order, OrderItem
from core.models import OrderStatus


@transaction.atomic
def checkout_cart(
        cart: Cart,
        buyer,
        shipping_address: Address,
        shipping_cost_per_order: Decimal = Decimal("0.00")
) -> List[Order]:
    items = list(CartItem.objects.select_related(
        "product", "product__seller")
                 .select_for_update().
                 filter(cart=cart))
    if not items:
        return []
    groups: Dict[int, list[CartItem]] = defaultdict(list)
    for it in items:
        groups[it.product.seller_id].append(it)
    created_orders: List[Order] = []
    for seller_id, seller_items in groups.items():
        subtotal = Decimal("0.00")
        currency = seller_items[0].product.currency
        # compliance check/reservation
        for it in seller_items:
            product = Product.objects.select_for_update().get(pk=it.product_id)
            if it.quantity > product.quantity:
                raise ValueError(f"Not enough goods '{product.title}'."
                                 f" Available: {product.quantity}")

            (Product.objects.filter(pk=product.pk).
             update(quantity=F('quantity') - it.quantity))
            subtotal += it.quantity * it.price_snapshot
        order = Order.objects.create(
            buyer=buyer,
            seller_id=seller_id,
            status=OrderStatus.CREATED,
            subtotal=subtotal,
            shipping_cost=shipping_cost_per_order,
            total=subtotal + shipping_cost_per_order,
            currency=currency,
            shipping_address=shipping_address,
        )
        bulk_items = []
        for it in seller_items:
            bulk_items.append(OrderItem(
                order=order,
                product_id=it.product_id,
                product_title_snapshot=it.product.title,
                price_snapshot=it.price_snapshot,
                quantity=it.quantity,
                line_total=it.quantity * it.price_snapshot,
            ))
        OrderItem.objects.bulk_create(bulk_items)
        created_orders.append(order)
    CartItem.objects.filter(cart=cart).delete()
    return created_orders
