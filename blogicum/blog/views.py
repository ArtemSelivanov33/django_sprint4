from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog.forms import CommentForm, PostForm, UserEditForm
from blog.models import Category, Comment, Post, User
from blogicum import constants


def paginate_by(request, post_obj):
    """Пагинация постов."""
    paginator = Paginator(post_obj, constants.POSTS_BY_PAGE)
    return paginator.get_page(request.GET.get("page"))


def index(request):
    """Главная страница."""
    posts = (
        Post.objects.all()
        .filter(
            category__is_published=True,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by("-pub_date")
        .annotate(comment_count=Count("comments"))
    ).select_related("category", "author", "location")
    return render(
        request,
        "blog/index.html",
        context={
            "posts": posts,
            "page_obj": paginate_by(request, posts),
        },
    )


def profile(request, username):
    """Страница пользователя."""
    user = get_object_or_404(
        User,
        is_active=True,
        username=username,
    )
    posts = (
        Post.objects.filter(author=user)
        .order_by("-pub_date")
        .annotate(comment_count=Count("comments"))
    )
    return render(
        request,
        "blog/profile.html",
        context={
            "profile": user,
            "page_obj": paginate_by(request, posts),
        },
    )


@login_required
def edit_profile(request):
    """Страница редактирования профиля."""
    user = get_object_or_404(
        User,
        username=request.user,
    )
    form = UserEditForm(
        request.POST or None,
        instance=user,
    )

    if form.is_valid():
        form.save()

    return render(
        request,
        "blog/user.html",
        context={
            "form": form,
            "profile": user,
        },
    )


@login_required
def create_post(request):
    """Публикация новых записей."""
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()
        return redirect(
            "blog:profile",
            username=request.user,
        )
    return render(
        request,
        "blog/create.html",
        {"form": form},
    )


@login_required
def edit_post(request, post_id):
    """Редактирование поста."""
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect("blog:post_detail", post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )

    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id)
    return render(
        request,
        "blog/create.html",
        context={
            "form": form,
            "post": post,
        },
    )


@login_required
def delete_post(request, post_id):
    """Удаление поста."""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect("blog:post_detail", post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:index")
    return render(
        request,
        "blog/create.html",
        context={"form": PostForm(instance=post)},
    )


def post_detail(request, post_id):
    """Отдельная страница публикации."""
    post = get_object_or_404(
        Post.objects.select_related(
            "category",
            "author",
            "location",
        ),
        id=post_id,
    )
    if post.author == request.user:
        comments = Comment.objects.filter(post_id=post_id)
    else:
        post = get_object_or_404(
            Post.objects.select_related(
                "category",
                "location",
                "author",
            ).filter(
                pub_date__lte=timezone.now(),
                category__is_published=True,
                is_published=True,
                id=post_id,
            )
        )
        comments = Comment.objects.filter(post_id=post_id)
    return render(
        request,
        "blog/detail.html",
        context={
            "post": post,
            "comments": comments,
            "form": CommentForm(),
        },
    )


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category.objects.filter(
            is_published=True,
            slug=category_slug,
        )
    )
    posts = (
        Post.objects.select_related(
            "category",
            "author",
            "location",
        )
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category=category,
        )
        .order_by("-pub_date")
    )
    return render(
        request,
        "blog/category.html",
        context={
            "category": category,
            "page_obj": paginate_by(request, posts),
        },
    )


@login_required
def add_comment(request, post_id):
    """Страница добавления комментария."""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("blog:post_detail", post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect("blog:post_detail", post_id)
    form = CommentForm(
        request.POST or None, files=request.FILES or None, instance=comment
    )
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id)
    return render(
        request,
        "blog/comment.html",
        context={
            "form": form,
            "comment": comment,
        },
    )


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментариев."""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect("blog:post_detail", post_id)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id)
    return render(request, "blog/comment.html")
