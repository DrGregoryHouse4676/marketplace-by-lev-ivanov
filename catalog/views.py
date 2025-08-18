from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import AddToCartForm, SellerProductForm
from accounts.models import SellerProfile
from core.models import SellerStatus

class ProductListView(ListView):
    template_name = "catalog/product_list.html"
    paginate_by = 20
    def get_queryset(self):
        qs = (Product.objects.filter(
            is_active=True,
            quantity__gt=0)
              .select_related('category', 'seller'))
        q = self.request.GET.get('q')
        cat = self.request.GET.get('category')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if cat:
            qs = qs.filter(category_id=cat)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['active_category'] = int(self.request.GET.get('category')) if self.request.GET.get('category') else None
        return ctx

class ProductDetailView(DetailView):
    template_name = 'catalog/product_detail.html'
    queryset = Product.objects.filter(is_active=True)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['add_form'] = AddToCartForm(initial={'product_id': self.object.id, 'quantity': 1})
        return ctx

# Seller cabinet (minimum): list/create products
@login_required
def seller_products(request):
    sp = getattr(request.user, 'seller_profile', None)
    if not sp or sp.status != SellerStatus.APPROVED:
        return redirect('seller_status')
    items = Product.objects.filter(seller=sp)
    return render(request, 'catalog/seller_products.html', {'items': items})

@login_required
def seller_product_create(request):
    sp = getattr(request.user, 'seller_profile', None)
    if not sp or sp.status != SellerStatus.APPROVED:
        return redirect('seller_status')
    if request.method == 'POST':
        form = SellerProductForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.seller = sp
            obj.is_active = False
            obj.save()
            return redirect('seller_products')
    else:
        form = SellerProductForm()
    return render(request, 'catalog/seller_product_form.html', {'form': form})
