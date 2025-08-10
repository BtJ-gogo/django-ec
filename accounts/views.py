from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import ShippingAddress
from .forms import ShippingAddressForm


class MypageView(TemplateView):
    template_name = "mypage.html"


class ShippingAddressView(ListView):
    model = ShippingAddress
    template_name = "shipping_address_list.html"


class ShippingAddressAddView(CreateView):
    model = ShippingAddress
    template_name = "shipping_address_add.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("accounts:shipping")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
