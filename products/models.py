from django.db import models
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


class Book(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "AC", "Active"
        DRAFT = "DR", "Draft"
        DELETE = "DE", "Delete"

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    publisher = models.CharField(max_length=50)
    publication_date = models.DateField()
    price = models.IntegerField()
    # price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="book_image/")
    stock = models.PositiveSmallIntegerField()
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:book_detail", kwargs={"pk": self.id})
