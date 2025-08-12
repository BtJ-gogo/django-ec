from django.urls import path

from .views import OrderView, AddressSelectView, OrderCanceledView, OrderCompletedView

app_name = "orders"

urlpatterns = [
    path("completed/", OrderCompletedView.as_view(), name="order_completed"),
    path("canceled/", OrderCanceledView.as_view(), name="order_canceled"),
    path("address/", AddressSelectView.as_view(), name="address_select"),
    path("", OrderView.as_view(), name="order"),
]
