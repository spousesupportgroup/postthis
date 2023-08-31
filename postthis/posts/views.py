from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Post


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "post_list"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


post_list_view = PostList.as_view()


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post-detail.html"
    context_object_name = "post"


post_detail_view = PostDetail.as_view()


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ["title", "slug", "status", "content"]
    success_message = _("Information successfully updated")
    template_name = "posts/post-form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.created_on = timezone.now()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        slug = self.object.slug
        return reverse_lazy("posts:post_detail", kwargs={"slug": slug})


post_create_view = PostCreateView.as_view()


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = "__all__"
    success_message = _("Information successfully updated")
    template_name = "posts/post-update.html"

    def get_success_url(self, **kwargs) -> str:
        return reverse("posts:post_detail", kwargs={"slug": self.request.POST.get("slug")})


post_update_view = PostUpdateView.as_view()


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("allposts")


post_delete_view = PostDeleteView.as_view()
