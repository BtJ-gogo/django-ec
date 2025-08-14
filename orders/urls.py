from django.urls import path

from .views import (
    OrderView,
    AddressSelectView,
    OrderCanceledView,
    OrderCompletedView,
    stripe_webhook,
)

app_name = "orders"

urlpatterns = [
    path("webhook/", stripe_webhook, name="stripe-webhook"),
    path("completed/", OrderCompletedView.as_view(), name="order_completed"),
    path("canceled/", OrderCanceledView.as_view(), name="order_canceled"),
    path("address/", AddressSelectView.as_view(), name="address_select"),
    path("", OrderView.as_view(), name="order"),
]
