from django.db import models

from catalog.models import Book
from users.models import User

RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class BookRatingManager(models.Manager):
    def get_rating_of_book(self, book):
        result = (
            self.get_queryset()
            .filter(book=book)
            .aggregate(
                book_rating_avg=models.Avg('rating'),
                book_rating_num=models.Count('user')
                )
            )
        if result['book_rating_avg']:
            result['book_rating_avg'] = round(result['book_rating_avg'], 2)
        return result

    def get_rating_of_user(self, book, user):
        if user.is_authenticated:
            return self.get_queryset().filter(book=book, user=user).first()


class BookRating(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name='книга',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE
    )
    rating = models.SmallIntegerField('оценка', choices=RATING_CHOICES)

    objects = BookRatingManager()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('book', 'user'), name='book_user_unique'
            ),
        )

    def __str__(self):
        return str(self.rating)
