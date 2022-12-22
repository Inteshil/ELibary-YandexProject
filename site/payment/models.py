from django.db import models

from users.models import User
from catalog.models import Book


class PurchasedBook(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE
        )
    book = models.ForeignKey(
        Book, verbose_name='книга', on_delete=models.CASCADE
        )

    class Meta:
        default_related_name = 'purchased'
        constraints = (
            models.UniqueConstraint(
                fields=('book', 'user'), name='purchased_book_unique'
            ),
        )
