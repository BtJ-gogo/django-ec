from django.views.generic import ListView, TemplateView

from .models import ShippingAddress


class MypageView(TemplateView):
    template_name = "mypage.html"


class ShippingAddressView(ListView):
    model = ShippingAddress
    template_name = "shipping_address_list.html"
