import pytest
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest, HttpResponseRedirect
from django.test import Client, RequestFactory
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from postthis.posts.forms import PostForm
from postthis.posts.models import Post, User
from postthis.posts.tests.factories import UserFactory
from postthis.posts.views import PostCreateView, PostUpdateView, post_detail_view, post_list_view

pytestmark = pytest.mark.django_db


class TestPostCommon:
    def test_authenticated_get_post_list(self, user: User, rf: RequestFactory):
        request = rf.get(reverse("posts:post_list"))
        request.user = UserFactory()
        response = post_list_view(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated_get_post_list(self, user: User, rf: RequestFactory):
        request = rf.get(reverse("posts:post_list"))
        request.user = AnonymousUser()
        response = post_list_view(request, username=user.username)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/posts/"


class TestPostCreateView:
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username="user1")

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = PostCreateView()
        request = rf.get(reverse("posts:post_create"))

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        # Initialize the form
        data = {
            "title": "Test-Title",
            "slug": "Test-Slug",
            "author": user,
            "content": "Test-Content",
            "status": 0,
        }
        form = PostForm(data)
        form.cleaned_data = {}
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]

        assert messages_sent == [_("Information successfully updated")]
        assert view.get_success_url() == f"/posts/{data['slug']}/"


class TestPostDetailView:
    def test_post_detail_view(self, user: User, rf: RequestFactory):
        post = Post.objects.create(
            title="The Catcher in the Rye", slug="TheCatcherInTheRye", author=user, content="Sample-Content", status=0
        )
        request = rf.get(reverse("posts:post_detail", kwargs={"slug": post.slug}))
        request.user = user

        response = post_detail_view(request, slug=post.slug)

        assert response.status_code == 200
        assert post.content in response.context_data["post"].content


class TestPostUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: User, rf: RequestFactory, client: Client):
        view = PostUpdateView()
        post = Post.objects.create(
            title="The Catcher in the Rye", slug="TheCatcherInTheRye", author=user, content="Sample-Content", status=0
        )

        request = rf.post(
            reverse("posts:post_update", kwargs={"slug": post.slug}),
            {
                "title": "The Catcher in the Rye",
                "author": user,
                "slug": "YetAnotherSlug",
                "content": "UpdatedSample-Content",
                "status": 1,
            },
        )
        request.user = user
        view.setup(request)

        assert view.get_success_url() == "/posts/YetAnotherSlug/"

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = PostUpdateView()
        request = rf.get("/fake-url/")

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        # Initialize the form
        data = {
            "title": "Test-Title",
            "slug": "Test-Slug",
            "author": user,
            "content": "Test-Content",
            "status": 0,
        }
        form = PostForm(data)
        form.cleaned_data = {}
        view.form_valid(form)

        messages_sent = [m.message for m in messages.get_messages(request)]
        assert messages_sent == [_("Information successfully updated")]
