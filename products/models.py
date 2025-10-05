from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)
    kana_name = models.CharField(max_length=50, blank=True)
    # romaji_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:author_detail", kwargs={"pk": self.pk})
    
    def clean(self):
        super().clean()
        if self.birth_date > timezone.now().date():
            raise ValidationError({'birth_date': 'Birth date cannot be in the future.'})

class Book(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "AC", "Active"
        DRAFT = "DR", "Draft"
        DELETE = "DE", "Delete"

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    publisher = models.CharField(max_length=50)
    published_at = models.DateField(db_index=True)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="book_image/", blank=True)
    stock = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:book_detail", kwargs={"pk": self.id})
