from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

from products.models import Book


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ["user", "product"]

    def get_total_price(self):
        return self.product.price * self.quantity
