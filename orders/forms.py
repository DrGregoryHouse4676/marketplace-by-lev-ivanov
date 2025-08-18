from django import forms
from accounts.models import Address

class CheckoutForm(forms.Form):
    shipping_address = forms.ModelChoiceField(queryset=Address.objects.none())
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["shipping_address"].queryset = Address.objects.filter(user=user)
