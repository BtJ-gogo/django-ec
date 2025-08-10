from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from carts.models import Cart

from accounts.forms import ShippingAddressForm


class OrderView(LoginRequiredMixin, FormMixin, ListView):
    model = Cart
    template_name = "order.html"
    form_class = ShippingAddressForm

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = 0
        for row in self.object_list:
            total += row.get_total_price()
        context["total"] = total
        return context
