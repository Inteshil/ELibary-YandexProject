from django.db import models


class BookManager(models.Manager):
    def enabled(self):
        return (
            self.get_queryset()
            .filter(is_published=True, is_blocked=False)
            .select_related('author')
            .prefetch_related('tags')
            )
