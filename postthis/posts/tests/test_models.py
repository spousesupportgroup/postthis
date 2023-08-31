from django.test import TestCase

from postthis.posts.models import Post


class PostTestCase(TestCase):
    def test_posts_str(self):
        test_post = Post(title="TestPost")
        assert str(test_post) == "TestPost"

    def test_posts_get_absolute_url(self):
        test_post = Post(title="TestPost", slug="TestPost")

        assert test_post.get_absolute_url() == f"/posts/{test_post.slug}/"
