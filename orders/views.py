import stripe

from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.conf import settings

from accounts.models import ShippingAddress
from carts.models import Cart


# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 配送先
        address_id = self.request.session.get("selected_address_id", None)
        print(address_id)
        if address_id:
            address = get_object_or_404(
                ShippingAddress, user=self.request.user, id=address_id
            )
        else:
            address = ShippingAddress.objects.filter(
                user=self.request.user, is_default=True
            ).first()
        if not address:
            messages.info(request, "配送先住所を登録してください。")
            return redirect(
                f"{reverse('accounts:shipping_add')}?next={reverse('orders:order')}"
            )
        # カート情報
        cart_list = Cart.objects.filter(user=self.request.user).prefetch_related(
            "product"
        )
        # 合計金額
        total = 0
        for row in cart_list:
            total += row.get_total_price()
        # del self.request.session["selected_address_id"]
        # クレジットカード
        return render(
            request,
            "order.html",
            {"address": address, "cart_list": cart_list, "total": total},
        )

    def post(self, request, *args, **kwargs):
        success_url = request.build_absolute_uri(reverse("orders:order_completed"))
        cancel_url = request.build_absolute_uri(reverse("orders:order_canceled"))

        session_data = {
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }

        cart_list = Cart.objects.filter(user=self.request.user).prefetch_related(
            "product"
        )
        if not cart_list.exists():
            return redirect(reverse("products:book_list"))

        for cart in cart_list:
            session_data["line_items"].append(
                {
                    "price_data": {
                        "currency": "jpy",
                        "product_data": {"name": cart.product.name},
                        "unit_amount": int(cart.product.price),
                    },
                    "quantity": cart.quantity,
                }
            )
        session = stripe.checkout.Session.create(**session_data)
        return redirect(session.url)


class AddressSelectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        address_list = ShippingAddress.objects.filter(user=self.request.user)

        return render(request, "address_select.html", {"address_list": address_list})

    def post(self, request, *args, **kwargs):
        selected_address_id = self.request.POST.get("address")

        if not selected_address_id:
            messages.error(request, "配送先を選択してください。")
            return redirect("orders:address_select")

        get_object_or_404(
            ShippingAddress,
            user=self.request.user,
            id=selected_address_id,
        )
        self.request.session["selected_address_id"] = selected_address_id
        return redirect(reverse("orders:order"))


class OrderCompletedView(TemplateView):
    template_name = "order_completed.html"


class OrderCanceledView(TemplateView):
    template_name = "order_canceled.html"
