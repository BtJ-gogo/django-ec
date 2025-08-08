from django import forms


class AddCartForm(forms.Form):
    quantity = forms.IntegerField(label="数量")

    def __init__(self, stock=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock = stock
        self.fields["quantity"].widget = forms.Select(
            choices=[(i, str(i)) for i in range(1, stock + 1)]
        )

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]
        if not (1 <= quantity <= self.stock):
            raise forms.ValidationError("在庫数を超えています。")
        return quantity
