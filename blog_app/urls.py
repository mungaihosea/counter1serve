from django.urls import path
from .views import homepage, login, detail_view, register, create_post

urlpatterns = [
    path("", homepage, name="homepage"),
    path("detail/<slug:id>/", detail_view, name="detail"),
    path("login/", login, name="login_user"),
    path("register/", register, name="register"),
    path("create_post/", create_post, name="new_post"),
]