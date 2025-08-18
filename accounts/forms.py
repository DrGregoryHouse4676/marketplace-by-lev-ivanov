from django import forms
from .models import Address, SellerProfile

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("type", "is_default", "line1", "line2", "city", "region", "postal_code", "country")

class SellerApplicationForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ("display_name", "description")
