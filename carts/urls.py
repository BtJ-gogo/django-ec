from django.urls import path

from .views import AddCartView, CartView, item_delete

app_name = "carts"

urlpatterns = [
    path("delete/<int:pk>/", item_delete, name="delete_cart"),
    path("add/<int:pk>/", AddCartView.as_view(), name="add_cart"),
    path("", CartView.as_view(), name="cart"),
]
