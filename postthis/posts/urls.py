from django.urls import path

from postthis.posts.views import post_create_view, post_delete_view, post_detail_view, post_list_view, post_update_view

app_name = "posts"
urlpatterns = [
    path("", view=post_list_view, name="post_list"),
    path("new/", view=post_create_view, name="post_create"),
    path("<slug:slug>/", view=post_detail_view, name="post_detail"),
    path("<slug:slug>/update", view=post_update_view, name="post_update"),
    path("<slug:slug>/delete", view=post_delete_view, name="post_delete"),
]
