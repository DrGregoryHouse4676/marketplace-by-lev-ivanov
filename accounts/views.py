from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import AddressForm, SellerApplicationForm
from .models import Address, SellerProfile

@login_required
def addresses(request):
    items = Address.objects.filter(user=request.user)
    return render(request, 'accounts/addresses.html', {'items': items})

@login_required
def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            messages.success(request, "Address created successfully")
            return redirect('accounts_addresses')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form})

@login_required
def seller_apply(request):
    # If you already have a profile, show your status
    sp = getattr(request.user, "seller_profile", None)
    if sp:
        return render(request, "accounts/seller_status.html", {"seller": sp})
    if request.method == "POST":
        form = SellerApplicationForm(request.POST)
        if form.is_valid():
            sp = form.save(commit=False)
            sp.user = request.user
            sp.save()
            messages.info(request, "Application submitted. Please wait for moderation.")
            return redirect("seller_statu")
    else:
        form = SellerApplicationForm()
    return render(request, "accounts/seller_apply.html", {"form": form})

@login_required
def seller_status(request):
    sp = getattr(request.user, "seller_profile", None)
    return render(request, "accounts/seller_status.html", {"seller": sp})
