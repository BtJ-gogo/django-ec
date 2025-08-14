from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

from products.models import Book


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PE", "Pending"
        UNPAID = "UN", "Unpaid"
        PAID = "PA", "Paid"
        SHIPPED = "SH", "Shipped"
        DELIVERED = "DE", "Delivered"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.PENDING)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    zipcode = models.CharField(max_length=8)
    state = models.CharField(max_length=10)
    city = models.CharField(max_length=30)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50, blank=True)
    stripe_id = models.CharField(max_length=250, blank=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
