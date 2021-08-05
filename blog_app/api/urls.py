from django.urls import path
from .api_views import (
    api_list_view,
    api_detail_view,
    api_create_view,
    api_delete_view,
    api_edit_view,
    api_adduser_view,
    ApiListView
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('list', ApiListView.as_view(), name="list_view"),
    path('detail/<slug>', api_detail_view, name = "detail_view"),
    path('create_post', api_create_view, name = "create_post"),
    path('delete/<slug>', api_delete_view, name = "delete_post"),
    path('edit/<slug>', api_edit_view, name="edit_post"),
    path('add_user', api_adduser_view, name="add_user"),
    path('login', obtain_auth_token, name="login")
]