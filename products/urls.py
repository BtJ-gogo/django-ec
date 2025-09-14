from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AuthorDetailView,
    BookListView,
    BookDetailView,
    FavoriteToggleView,
    BookListLoadView,
)

app_name = "products"

urlpatterns = [
    path("books/load/", BookListLoadView.as_view(), name="product_list_load"),
    path("books/<str:category>/load/", BookListLoadView.as_view(), name="book_list_load"),
    path("favorite/<int:pk>/", FavoriteToggleView.as_view(), name="favorite_toggle"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author_detail"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/<str:category>/", BookListView.as_view(), name="book_list"),
]
