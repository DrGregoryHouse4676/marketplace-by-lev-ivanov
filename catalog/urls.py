from django.urls import path
from .views import ProductListView, ProductDetailView, seller_products, seller_product_create

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('p/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('seller/products/', seller_products, name='seller_products'),
    path('seller/products/new/', seller_product_create, name='seller_product_create'),
]
