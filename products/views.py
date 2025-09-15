from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Author, Book
from accounts.models import Favorite
from .forms import AddCartForm


class SearchRedirectMixin:
    search_param = "search"
    search_redirect_url_name = "products:book_list"

    def dispatch(self, request, *args, **kwargs):
        search = request.GET.get(self.search_param)
        redirect_url = (
            f"{reverse(self.search_redirect_url_name)}?{self.search_param}={search}"
        ) if search and self.search_redirect_url_name else None

        if redirect_url and request.get_full_path() != redirect_url:
            return redirect(redirect_url)

        return super().dispatch(request, *args, **kwargs)



class BookListView(SearchRedirectMixin, ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 8

    def get_queryset(self):
        book_list = Book.objects.select_related("author", "category")

        category = self.kwargs.get("category")
        if category:
            return book_list.filter(category__name=category)

        search = self.request.GET.get("search")
        if search:
            book_list = book_list.filter(
                Q(name__icontains=search)
                | Q(author__kana_name__icontains=search)
                | Q(author__name__icontains=search)
            )

        return book_list


class BookListLoadView(View):
    def get(self, request, *args, **kwargs):
        page = int(self.request.GET.get("page", 1))
        book_list = Book.objects.select_related("author", "category")

        category = self.kwargs.get("category")
        if category:
            book_list = book_list.filter(category__name=category)

        search = self.request.GET.get("search")
        if search:
            book_list = book_list.filter(
                Q(name__icontains=search)
                | Q(author__kana_name__icontains=search)
                | Q(author__name__icontains=search)
            )

        paginator = Paginator(book_list, 8)
        if page > paginator.num_pages:
            return JsonResponse({"html": "", "has_next": False})
        page_obj = paginator.get_page(page)
            
        html = render_to_string("book_list_items.html", {"object_list": page_obj})
        return JsonResponse({"html": html, "has_next": page_obj.has_next()})        




class BookDetailView(SearchRedirectMixin, DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_queryset(self):
        return Book.objects.select_related("author", "category")

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


class AuthorDetailView(SearchRedirectMixin, DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = "author"
    paginate_by = 8
    search_redirect_url_name = "products:book_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        books = Book.objects.filter(author=context["author"]).select_related(
            "author", "category"
        )
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
            messages.info(request, f"お気に入りから削除しました。")
            result.delete()
        else:
            messages.info(request, f"お気に入りに追加しました。")

        return redirect("products:book_detail", pk=kwargs.get("pk"))
