from django.views.generic import ListView,
from django.shortcuts import render

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 20
