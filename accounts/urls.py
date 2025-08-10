from django.urls import path

from .views import MypageView, ShippingAddressView, ShippingAddressAddView

app_name = "accounts"

urlpatterns = [
    path("shipping/add/", ShippingAddressAddView.as_view(), name="shipping_add"),
    path("shipping/", ShippingAddressView.as_view(), name="shipping"),
    path("", MypageView.as_view(), name="mypage"),
]
