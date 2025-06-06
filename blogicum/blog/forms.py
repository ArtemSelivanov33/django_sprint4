from django.forms import DateTimeInput, ModelForm, Textarea

from blog.models import Comment, Post


class PostForm(ModelForm):
    """Форма поста."""

    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"},
            ),
        }


class CommentForm(ModelForm):
    """Форма комментария."""

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": Textarea(attrs={"rows": "5"}),
        }
