from django.contrib import admin

from .models import Author, Book, Category


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "price", "stock", "publication_date", "category"]
    list_editable = ["price", "stock"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
