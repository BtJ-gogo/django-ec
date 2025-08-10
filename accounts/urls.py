from django.urls import path

from .views import MypageView, ShippingAddressView

app_name = "accounts"

urlpatterns = [
    path("shipping/", ShippingAddressView.as_view(), name="shipping"),
    path("", MypageView.as_view(), name="mypage"),
]
