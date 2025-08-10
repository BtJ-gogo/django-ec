from django.urls import path

from .views import (
    MypageView,
    ShippingAddressView,
    ShippingAddressAddView,
    ShippingAddressUpdateView,
)

app_name = "accounts"

urlpatterns = [
    path("shipping/add/", ShippingAddressAddView.as_view(), name="shipping_add"),
    path(
        "shipping/update/<int:pk>",
        ShippingAddressUpdateView.as_view(),
        name="shipping_update",
    ),
    path("shipping/", ShippingAddressView.as_view(), name="shipping"),
    path("", MypageView.as_view(), name="mypage"),
]
