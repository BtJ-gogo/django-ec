from django.views import View
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Cart
from products.models import Book
from products.views import SearchRedirectMixin


class AddCartView(View):
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            book = get_object_or_404(Book, id=kwargs.get("pk"))
            try:
                quantity = int(self.request.POST.get("quantity"))
            except (ValueError, TypeError):
                quantity = 1

            try:
                cart = Cart.objects.get(user=self.request.user, product=book)
                if cart.quantity + quantity <= book.stock:
                    cart.quantity += quantity
                else:
                    # messageいれる
                    cart.quantity = book.stock
                cart.save()

            except Cart.DoesNotExist:
                cart = Cart(
                    user=self.request.user,
                    product=book,
                    quantity=quantity,
                )
                cart.save()

            # messages.success(request, f"カートに追加しました。")
            return redirect(reverse("carts:cart"))
        # これから作成
        else:
            return redirect(reverse("account_login"))


class CartListView(ListView):
    model = Cart
    template_name = "cart_list.html"

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related("product")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        for row in self.object_list:
            total += row.get_total_price()
        context["total"] = total
        return context


class CartView(SearchRedirectMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            view = CartListView.as_view()
            return view(request, *args, **kwargs)
        else:
            # message入れたほうがいいかも
            return redirect(reverse("account_login"))


@require_POST
def item_delete(request, pk):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, id=pk)
        if cart.exists():
            cart.delete()
            return redirect("carts:cart")
        else:
            messages.warning(request, "カートのアイテムが見つかりませんでした。")
            return redirect("carts:cart")
