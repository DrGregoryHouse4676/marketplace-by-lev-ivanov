from django.urls import path
from .views import checkout, orders_created, seller_shipments, set_tracking


urlpatterns = [
    path(
         "checkout/",
         checkout,
         name="checkout"
         ),
    path(
        "orders/created/",
        orders_created,
        name="orders_created"
    ),
    path(
        "seller/shipments/",
        seller_shipments,
        name="seller_shipments"),
    path(
        "seller/shipments/<int:order_id>/tracking/",
        set_tracking,
        name="set_tracking"),
]
