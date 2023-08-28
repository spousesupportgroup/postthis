from django.conf import settings
from django.contrib import admin
from django.urls import path

from postthis.posts.views import post_list_view, post_detail_view, post_update_view, post_create_view

app_name = "posts"
urlpatterns = [
    path("", view=post_list_view, name="post-list"),
    path("new/", view=post_create_view, name="post-create"),
    path("<slug:slug>/", view=post_detail_view, name="post-detail"),
    path("<slug:slug>/update", view=post_update_view, name="post-update"),
]
