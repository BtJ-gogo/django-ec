from django.urls import path

from .views import OrderView, AddressSelectView

app_name = "orders"

urlpatterns = [
    path("address/", AddressSelectView.as_view(), name="address_select"),
    path("", OrderView.as_view(), name="order"),
]
