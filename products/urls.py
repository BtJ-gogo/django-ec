from django.urls import path
from django.views.generic import TemplateView

from .views import AuthorDetailView, BookListView, BookDetailView

app_name = "products"

urlpatterns = [
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author_detail"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("books/", BookListView.as_view(), name="book_list"),
    path(
        "",
        TemplateView.as_view(template_name="product_home.html"),
        name="product_home",
    ),
]
