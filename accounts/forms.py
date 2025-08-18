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
            "is_default",
        ]
        labels = {
            "last_name": "姓",
            "first_name": "名",
            "last_kana_name": "セイ",
            "first_kana_name": "メイ",
            "phone": "電話番号",
            "zipcode": "郵便番号",
            "state": "都道府県",
            "city": "市区町村",
            "address1": "番地・建物名等",
            "address2": "建物名等（任意）",
            "is_default": "デフォルト住所にする",
        }
