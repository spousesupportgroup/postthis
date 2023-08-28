from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, UpdateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Post
from .forms import PostForm


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post-list.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


post_list_view = PostList.as_view()


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post-detail.html"
    context_object_name = "post"


post_detail_view = PostDetail.as_view()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "slug", "status", "content"]

    template_name = "posts/post-form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created_on = timezone.now()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        slug = self.object.slug
        return reverse_lazy("posts:post-detail", kwargs={"slug": slug})


post_create_view = PostCreateView.as_view()


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = "__all__"
    template_name = "posts/post-update.html"

    def get_success_url(self) -> str:
        slug = self.kwargs[self.slug_url_kwarg]
        return reverse_lazy("posts:post-detail", kwargs={"slug": slug})


post_update_view = PostUpdateView.as_view()


class PostDeleteView(LoginRequiredMixin, UpdateView):
    model = Post
    success_url = reverse_lazy("allposts")


post_update_view = PostUpdateView.as_view()
