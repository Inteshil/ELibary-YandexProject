from django.db import models


class BookManager(models.Manager):
    def enabled(self):
        return (
            self.get_queryset()
            .filter(is_published=True, is_blocked=False)
            .select_related('author')
            .prefetch_related('tags')
            )


class BookChapterManager(models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .order_by('number')
            .select_related('book')
            )

    def published_list(self):
        return list(self.published())
