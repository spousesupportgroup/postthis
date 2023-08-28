from postthis.posts.models import Post


def test_posts_str():
    test_post = Post(title="TestPost")
    assert str(test_post) == "TestPost"
