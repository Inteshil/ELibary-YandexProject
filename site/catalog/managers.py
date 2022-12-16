from django.db import models


class BookManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('author')
            .prefetch_related('tags')
            )

    def enabled(self):
        return (
            self.get_queryset()
            .filter(is_published=True, is_blocked=False)
            )

    def enabled_for_author(self, user):
        enabled_qs = self.enabled()
        if user.is_authenticated:
            author_qs = self.get_queryset().filter(author=user)
            return enabled_qs | author_qs
        return enabled_qs


class BookChapterManager(models.Manager):
    def published(self, book):
        return (
            self.get_queryset()
            .filter(
                book=book, is_published=True, book__is_blocked=False,
                book__is_published=True
                )
            .order_by('number')
            .select_related('book')
            )

    def for_user(self, user, book):
        published_qs = self.published(book)
        if user.is_authenticated:
            author_qs = self.get_queryset().filter(
                book=book, book__author=user
                )
            return published_qs | author_qs
        return published_qs

    def get_max_number(self):
        return self.aggregate(number=models.Max('number'))['number'] + 1
