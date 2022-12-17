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

    def get_max_number(self, book):
        qs = self.filter(book=book)
        max_number = qs.aggregate(number=models.Max('number'))['number']
        if max_number:
            return max_number + 1
        return 1

    def get_neighboring_chapters(self, queryset, chapter_id):
        previous = current = next = None
        for idx in range(len(queryset)):
            current_chapter = queryset[idx]
            if current_chapter.pk == chapter_id:
                current = current_chapter
                if idx != 0:
                    previous = queryset[idx - 1]
                if idx != len(queryset) - 1:
                    next = queryset[idx + 1]
                break
        return current, {'previous': previous, 'next': next}
