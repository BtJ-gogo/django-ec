from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
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


class ShippingAddressUpdateView(UpdateView):
    model = ShippingAddress
    template_name = "shipping_address_update.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("accounts:shipping")


class ShippingAddressDeleteView(View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(
            ShippingAddress, user=self.request.user, id=kwargs.get("pk")
        )
        print(obj.last_name)
        obj.delete()
        return redirect("accounts:shipping")
