from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect

from blog.models import Post
from blogicum import constants


def paginate_by(request, posts):
    """Пагинация постов."""
    paginator = Paginator(posts, constants.POSTS_BY_PAGE)
    return paginator.get_page(request.GET.get("page"))


def is_post_author(func):
    """Проверяет, является ли пользователь автором поста."""

    def wrapper(request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)
        if request.user != post.author:
            return redirect("blog:post_detail", post_id=post.id)
        return func(request, post_id, *args, **kwargs)

    return wrapper
