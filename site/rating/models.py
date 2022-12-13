from django.db import models

from catalog.models import Book
from users.models import User

RATING_CHOICES = (
    (1, 'Ненависть'),
    (2, 'Неприязнь'),
    (3, 'Нейтрально'),
    (4, 'Обожание'),
    (5, 'Любовь'),
)


class BookRatingManager(models.Manager):
    def get_rating_of_book(self, book):
        return (
            self.get_queryset()
            .filter(book=book)
            .aggregate(
                book_rating_avg=models.Avg('rating'),
                book_rating_num=models.Count('user')
                )
            )


class BookRating(models.Model):
    book = models.ForeignKey(
        Book, verbose_name='книга', on_delete=models.CASCADE
        )
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE
        )
    rating = models.SmallIntegerField('оценка', choices=RATING_CHOICES)

    objects = BookRatingManager()

    class Meta:
        unique_together = ('book', 'user',)

    def __str__(self):
        return str(self.rating)
