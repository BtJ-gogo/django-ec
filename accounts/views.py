from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme

from .models import ShippingAddress
from .forms import ShippingAddressForm
from orders.models import Order


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

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url, allowed_hosts=self.request.get_host()
        ):
            return next_url
        return super().get_success_url()


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


class OrderHistoryView(ListView):
    model = Order
    template_name = "order_history.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
