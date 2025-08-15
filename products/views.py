from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse

from .models import Author, Book
from accounts.models import Favorite
from .forms import AddCartForm


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


class BookDetailView(SearchRedirectMixin, DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"
    search_redirect_url_name = "products:book_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.stock > 0:
            form = AddCartForm(stock=self.object.stock)
            context["form"] = form
        else:
            context["form"] = None

        return context


class AuthorDetailView(SearchRedirectMixin, DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = "author"
    paginate_by = 10
    search_redirect_url_name = "products:book_list"

    # get_context_data()で著作一覧を取得して表示するようにする
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = context["author"].book_set.all()
        p = Paginator(books, self.paginate_by)

        page_number = self.request.GET.get("page")
        page = p.get_page(page_number)

        context["books"] = page
        return context


class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        result, created = Favorite.objects.get_or_create(
            user=self.request.user, product_id=kwargs.get("pk")
        )
        if not created:
            result.delete()

        return redirect("products:book_detail", pk=kwargs.get("pk"))
