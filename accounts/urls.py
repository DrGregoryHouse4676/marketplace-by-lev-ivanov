from django.urls import path
from . import views

urlpatterns = [
    path("account/addresses/", views.addresses, name="accounts_addresses"),
    path("account/addresses/new/", views.address_create, name="accounts_address_create"),
    path("seller/apply/", views.seller_apply, name="seller_apply"),
    path("seller/status/", views.seller_status, name="seller_status"),
]
