from django.urls import path

from .views import MypageView

app_name = "accounts"

urlpatterns = [
    path("", MypageView.as_view(), name="mypage"),
]
