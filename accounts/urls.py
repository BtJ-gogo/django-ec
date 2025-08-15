from django.urls import path

from .views import (
    MypageView,
    ShippingAddressView,
    ShippingAddressAddView,
    ShippingAddressUpdateView,
    ShippingAddressDeleteView,
    OrderHistoryView,
)

app_name = "accounts"

urlpatterns = [
    path("order/history/", OrderHistoryView.as_view(), name="order_history"),
    path("shipping/", ShippingAddressView.as_view(), name="shipping"),
    path("shipping/add/", ShippingAddressAddView.as_view(), name="shipping_add"),
    path(
        "shipping/update/<int:pk>",
        ShippingAddressUpdateView.as_view(),
        name="shipping_update",
    ),
    path(
        "shipping/delete/<int:pk>/",
        ShippingAddressDeleteView.as_view(),
        name="shipping_delete",
    ),
    path("", MypageView.as_view(), name="mypage"),
]
