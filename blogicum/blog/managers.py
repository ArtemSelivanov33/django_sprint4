from django.db.models import Manager, Q
from django.utils.timezone import now


class PostManager(Manager):
    """Менеджер фильтрующий запрос к БД."""

    def published_posts(self):
        """Возвращает опубликованные посты."""
        return self.filter(
            Q(is_published=True)
            & Q(pub_date__lte=now())
            & Q(category__is_published=True)
        )

    def get_user_posts(self, user=None):
        """Возвращает посты в зависимости от источника запроса."""
        return self.filter(
            Q(author=user) | ~Q(is_published=True)
        )


class CategoryManager(Manager):
    """Менеджер фильтрации постов в категории."""

    def filtered_posts(self):
        """Возвращает опубликованные посты в категории."""
        return self.filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True
        )
