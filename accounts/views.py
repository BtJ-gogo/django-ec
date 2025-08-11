from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ShippingAddress
from .forms import ShippingAddressForm


class MypageView(LoginRequiredMixin, TemplateView):
    template_name = "mypage.html"


class ShippingAddressView(LoginRequiredMixin, ListView):
    model = ShippingAddress
    template_name = "shipping_address_list.html"


class ShippingAddressAddView(LoginRequiredMixin, CreateView):
    model = ShippingAddress
    template_name = "shipping_address_add.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("accounts:shipping")

    def form_valid(self, form):
        form.instance.user = self.request.user

        if not ShippingAddress.objects.filter(user=self.request.user).exists():
            form.instance.is_default = True

        if form.instance.is_default:
            ShippingAddress.objects.filter(
                user=self.request.user, is_default=True
            ).update(is_default=False)

        return super().form_valid(form)


class ShippingAddressUpdateView(LoginRequiredMixin, UpdateView):
    model = ShippingAddress
    template_name = "shipping_address_update.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("accounts:shipping")

    def form_valid(self, form):
        if form.instance.is_default:
            ShippingAddress.objects.filter(
                user=self.request.user, is_default=True
            ).update(is_default=False)

        return super().form_valid(form)


class ShippingAddressDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(
            ShippingAddress, user=self.request.user, id=kwargs.get("pk")
        )
        obj.delete()
        return redirect("accounts:shipping")
