from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "date",
        "payment_status",
        "shipping_status",
        "total_price",
    ]
    list_editable = ["payment_status", "shipping_status"]
    search_fields = ["id", "user", "date"]
    list_filter = ["payment_status", "shipping_status"]
    inlines = [OrderItemInline]
