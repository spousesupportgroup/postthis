from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Mega:
        model = Post
        fields = "__all__"
