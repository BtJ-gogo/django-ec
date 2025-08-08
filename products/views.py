from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse

from .models import Book


class SearchMixin:
    search_param = "search"

    def get_queryset(self):
        search = self.request.GET.get(self.search_param)
        book_list = Book.objects.all()
        if search:
            book_list = book_list.filter(
                Q(name__icontains=search)
                | Q(author__kana_name__icontains=search)
                | Q(author__name__icontains=search)
            )
        return book_list


class SearchRedirectMixin:
    search_param = "search"
    search_redirect_url_name = None

    def dispatch(self, request, *args, **kwargs):
        search = request.GET.get(self.search_param)
        if search and self.search_redirect_url_name:
            redirect_url = (
                f"{reverse(self.search_redirect_url_name)}?{self.search_param}={search}"
            )
            return redirect(redirect_url)
        return super().dispatch(request, *args, **kwargs)


class BookListView(SearchMixin, ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 20
