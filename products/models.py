from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)


class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}({self.birth_date.strftime('%Y/%m/%d')})"
