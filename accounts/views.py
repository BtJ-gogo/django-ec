from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Prefetch
from django.contrib import messages

from .models import ShippingAddress, Favorite
from .forms import ShippingAddressForm
from orders.models import Order, OrderItem
from products.views import SearchRedirectMixin


class MypageView(LoginRequiredMixin, SearchRedirectMixin, TemplateView):
    template_name = "mypage.html"


class ShippingAddressView(LoginRequiredMixin, SearchRedirectMixin, ListView):
    model = ShippingAddress
    template_name = "shipping_address_list.html"

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)


class ShippingAddressAddView(LoginRequiredMixin, SearchRedirectMixin, CreateView):
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


class ShippingAddressUpdateView(LoginRequiredMixin, SearchRedirectMixin, UpdateView):
    model = ShippingAddress
    template_name = "shipping_address_update.html"
    form_class = ShippingAddressForm
    success_url = reverse_lazy("accounts:shipping")

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user)

    def form_valid(self, form):
        if form.instance.is_default:
            ShippingAddress.objects.filter(
                user=self.request.user, is_default=True
            ).update(is_default=False)

        return super().form_valid(form)


class ShippingAddressDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        del_obj = get_object_or_404(
            ShippingAddress, user=self.request.user, id=kwargs.get("pk")
        )
        del_obj.delete()

        if del_obj.is_default:
            obj = ShippingAddress.objects.filter(user=self.request.user).first()
            if obj:
                obj.is_default = True
                obj.save()
        return redirect("accounts:shipping")


class OrderHistoryView(LoginRequiredMixin, SearchRedirectMixin, ListView):
    model = Order
    template_name = "order_history.html"

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .exclude(payment_status="PE")
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
        )


class OrderDetailView(LoginRequiredMixin, SearchRedirectMixin, DetailView):
    model = Order
    template_name = "order_detail.html"

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
            .exclude(payment_status="PE")
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            )
        )


class FavoriteListView(LoginRequiredMixin, SearchRedirectMixin, ListView):
    model = Favorite
    template_name = "favorite_list.html"

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related(
            "product", "product__author"
        )


class FavoriteDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        result = get_object_or_404(
            Favorite, user=self.request.user, product_id=kwargs.get("pk")
        )
        result.delete()
        messages.success(
            request, f"{ result.product.name}をお気に入りから削除しました。"
        )
        return redirect("accounts:favorite_list")
