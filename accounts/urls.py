from django.views.generic import TemplateView
from django.urls import path
from .views import SignUpView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
]
