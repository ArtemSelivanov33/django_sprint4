from django.db.models import Manager, Q
from django.utils.timezone import now


class PostManager(Manager):
    """Менеджер фильтрующий запрос к БД."""

    def get_all_active_posts(self):
        return self.filter(
            Q(is_published=True)
            & Q(pub_date__lte=now())
            & Q(category__is_published=True)
        )

    def published_posts(self, user=None):
        """Возвращает посты в зависимости от того, кто запрашивает."""
        if user.is_authenticated:
            return self.filter(author=user)
        return self.get_all_active_posts()


class CategoryManager(Manager):
    """Менеджер фильтрации постов в категории."""

    def filtered_posts(self):
        return self.filter(
            is_published=True, pub_date__lte=now(), category__is_published=True
        )
