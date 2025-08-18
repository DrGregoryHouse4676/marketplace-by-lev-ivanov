from django.db.models import F
from .models import Cart, CartItem
from catalog.models import Product

def add_item(cart: Cart, product: Product, quantity: int) -> CartItem:
    quantity = max(int(quantity), 1)
    item, created = CartItem.objects.select_for_update().get_or_create(
        cart=cart, product=product,
        defaults={"quantity": quantity, "price_snapshot": product.price},
    )
    if not created:
        item.quantity = F("quantity") + quantity
    item.price_snapshot = product.price
    item.save(update_fields=["quantity", "price_snapshot", "updated_at"])
    item.refresh_from_db()
    return item

def update_item(cart: Cart, product: Product, quantity: int) -> CartItem | None:
    if quantity <= 0:
        CartItem.objects.filter(cart=cart, product=product).delete()
        return None
    item, _ = CartItem.objects.get_or_create(
        cart=cart, product=product,
        defaults={"quantity": quantity, "price_snapshot": product.price},
    )
    item.quantity = quantity
    item.price_snapshot = product.price
    item.save(update_fields=["quantity", "price_snapshot", "updated_at"])
    return item
