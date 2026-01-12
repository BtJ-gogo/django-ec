import stripe

from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.db import transaction

from accounts.models import ShippingAddress
from carts.models import Cart
from .models import Order, OrderItem


# create the Stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # 配送先
        address_id = self.request.session.get("selected_address_id", None)

        if address_id:
            try:
                address = ShippingAddress.objects.get(
                    user=self.request.user, id=address_id
                )
            except ShippingAddress.DoesNotExist:
                address = ShippingAddress.objects.filter(
                    user=self.request.user, is_default=True
                ).first()

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
        cart_list = Cart.objects.filter(user=self.request.user).select_related(
            "product"
        )
        # 合計金額
        total = 0
        for row in cart_list:
            total += row.get_total_price()

        return render(
            request,
            "order.html",
            {"address": address, "cart_list": cart_list, "total": total},
        )

    @method_decorator(transaction.atomic)
    def post(self, request, *args, **kwargs):
        success_url = request.build_absolute_uri(reverse("orders:order_completed"))
        cancel_url = request.build_absolute_uri(reverse("orders:order_canceled"))

        session_data = {
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }

        cart_list = Cart.objects.filter(user=self.request.user).select_related(
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
        # Create Order
        address_id = self.request.session.get("selected_address_id", None)
        if address_id:
            address = get_object_or_404(
                ShippingAddress, user=self.request.user, id=address_id
            )
        else:
            address = get_object_or_404(
                ShippingAddress, user=self.request.user, is_default=True
            )
        order = Order.objects.create(
            user=self.request.user,
            name=address.last_name + " " + address.first_name,
            email=address.user.email,
            phone=address.phone,
            zipcode=address.zipcode,
            state=address.get_state_display(),
            city=address.city,
            address1=address.address1,
            address2=address.address2,
            total_price=sum(cart.get_total_price() for cart in cart_list),
        )
        # Product Info to OrderItem
        for cart in cart_list:
            OrderItem.objects.create(
                order=order,
                product=cart.product,
                price=cart.product.price,
                quantity=cart.quantity,
            )
        session_data["client_reference_id"] = str(order.id)
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


class OrderCompletedView(LoginRequiredMixin, TemplateView):
    template_name = "order_completed.html"


class OrderCanceledView(LoginRequiredMixin, TemplateView):
    template_name = "order_canceled.html"


@csrf_exempt
@transaction.atomic
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    
    if event.type == "checkout.session.completed":
        session = event.data.object
        if session.mode == "payment" and session.payment_status == "paid":
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            
            if order.payment_status == "PA":
                return HttpResponse(status=200)
            
            order.payment_status = "PA"
            order.stripe_id = session.payment_intent
            order.save()
            Cart.objects.filter(user=order.user).delete()
            request.session.pop("selected_address_id", None)

    return HttpResponse(status=200)
