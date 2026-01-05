from django.views.generic import View
from django.shortcuts import render
from django.db.models import Count

from products.models import Book


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = {
            "new_books": Book.objects.all()
            .order_by("-published_at")
            .select_related("author")[:4],
        }
        context["favorite_books"] = (
            Book.objects.annotate(fav_count=Count("favorite"))
            .order_by("-fav_count", "-published_at")
            .select_related("author")[:4]
        )
        return render(request, "home.html", context)
