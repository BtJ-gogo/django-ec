from django import forms

from accounts.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "last_name",
            "first_name",
            "last_kana_name",
            "first_kana_name",
            "phone",
            "zipcode",
            "state",
            "city",
            "address1",
            "address2",
        ]
