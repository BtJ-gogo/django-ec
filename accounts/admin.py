from django.contrib import admin
from .models import CustomUser, ShippingAddress


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )


@admin.register(ShippingAddress)
class ShippingAdressAdmin(admin.ModelAdmin):
    pass
