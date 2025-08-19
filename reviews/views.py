from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from .models import Review
from catalog.models import Product
from orders.models import OrderItem
from core.models import OrderStatus


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "comment")


@login_required
def create_review(request, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    can_review = OrderItem.objects.filter(
        product=product,
        order__buyer=request.user,
        order__status=OrderStatus.DELIVERED
    ).exists()
    if not can_review:
        return redirect(product.get_absolute_url())
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                product=product, buyer=request.user,
                defaults={"rating": form.cleaned_data["rating"],
                          "comment": form.cleaned_data.get("comment")}
            )
            return redirect(product.get_absolute_url())
    else:
        form = ReviewForm()
    return render(
        request,
        "reviews/create.html", {"form": form, "product": product})
