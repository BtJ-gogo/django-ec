from django.urls import path

from .views import (
    MypageView,
    ShippingAddressView,
    ShippingAddressAddView,
    ShippingAddressUpdateView,
    ShippingAddressDeleteView,
)

app_name = "accounts"

urlpatterns = [
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
    path("shipping/", ShippingAddressView.as_view(), name="shipping"),
    path("", MypageView.as_view(), name="mypage"),
]
