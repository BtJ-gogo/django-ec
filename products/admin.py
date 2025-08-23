from django.contrib import admin

from .models import Author, Book, Category


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "price", "stock", "published_at", "category"]
    list_editable = ["price", "stock"]
    search_fields = ["name", "author__name"]
    list_filter = ["category"]
    ordering = ["price", "stock", "published_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]
