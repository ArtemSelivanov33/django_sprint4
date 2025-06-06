from django.contrib.auth import get_user_model
from django.db import models

from blog import managers
from blogicum import constants

User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено",
    )

    class Meta:
        abstract = True


class Post(PublishedModel):
    objects = managers.PostManager()
    title = models.CharField(
        max_length=constants.MAX_FIELD_LENGTH,
        verbose_name="Заголовок",
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",
    )
    location = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="posts",
    )
    image = models.ImageField(
        verbose_name="Картинка публикации",
        upload_to="post_images",
        blank=True,
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title[: constants.MAX_TITLE_LENGTH]


class Category(PublishedModel):
    objects = managers.CategoryManager()
    title = models.CharField(
        max_length=constants.MAX_FIELD_LENGTH,
        verbose_name="Заголовок",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        ordering = ("title",)

    def __str__(self):
        return f"{self.title[:constants.MAX_TITLE_LENGTH]}"


class Location(PublishedModel):
    name = models.CharField(
        max_length=constants.MAX_FIELD_LENGTH,
        verbose_name="Название места",
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ("name",)

    def __str__(self):
        return self.name[: constants.MAX_NAME_LENGTH]


class Comment(models.Model):
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Комментируемый пост",
        related_name="comments",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)

    def __str__(self):
        return (
            f"{self.author}: "
            f"{self.text[:constants.MAX_DESCRIPTION_LENGTH]}"
        )
