from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse

from .models import Author, Book
from accounts.models import Favorite
from .forms import AddCartForm


class SearchRedirectMixin:
    search_param = "search"
    search_redirect_url_name = "products:book_list"

    def dispatch(self, request, *args, **kwargs):
        search = request.GET.get(self.search_param)
        if search and self.search_redirect_url_name:
            redirect_url = (
                f"{reverse(self.search_redirect_url_name)}?{self.search_param}={search}"
            )
            return redirect(redirect_url)
        return super().dispatch(request, *args, **kwargs)


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 20

    def get_queryset(self):
        book_list = Book.objects.all()

        search = self.request.GET.get("search")
        if search:
            book_list = book_list.filter(
                Q(name__icontains=search)
                | Q(author__kana_name__icontains=search)
                | Q(author__name__icontains=search)
            )

        category = self.kwargs.get("category")
        if category:
            return book_list.filter(category__name=category)

        return book_list


class BookDetailView(SearchRedirectMixin, DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.stock > 0:
            form = AddCartForm(stock=self.object.stock)
            context["form"] = form
        else:
            context["form"] = None

        if self.request.user.is_authenticated:
            favorite = self.object.favorite_set.filter(user=self.request.user).exists()
            context["favorite"] = favorite
        else:
            context["favorite"] = None

        books = Book.objects.filter(author=self.object.author).exclude(
            pk=self.object.pk
        )[:5]
        context["other_books"] = books

        return context


class BookCategoryView(SearchRedirectMixin, ListView):
    model = Book
    template_name = "book_category.html"

    def get_queryset(self):
        category = self.kwargs.get("category")
        return Book.objects.filter(category__name=category)


class AuthorDetailView(SearchRedirectMixin, DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = "author"
    paginate_by = 6
    search_redirect_url_name = "products:book_list"

    # get_context_data()で著作一覧を取得して表示するようにする
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = context["author"].book_set.all()
        p = Paginator(books, self.paginate_by)

        page_number = self.request.GET.get("page")
        page = p.get_page(page_number)

        context["page_obj"] = page
        return context


class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        result, created = Favorite.objects.get_or_create(
            user=self.request.user, product_id=kwargs.get("pk")
        )
        if not created:
            result.delete()

        return redirect("products:book_detail", pk=kwargs.get("pk"))
