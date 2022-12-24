from django.db import models
from django.db.models.functions import Length

from users.models import User
from catalog.models import Book


class QuoteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('book', 'user')

    def for_catalog(self):
        ''' Убираем слишком маленькие цитаты '''

        return (
            self.get_queryset()
            .annotate(text_len=Length('text'))
            .filter(text_len__gte=20)
            .filter(text_len__lte=2000)
            )


class Quote(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book, verbose_name='книга', on_delete=models.CASCADE
    )
    text = models.CharField('текст', max_length=1000)
    creation_date = models.DateTimeField('дата создания', auto_now_add=True)

    objects = QuoteManager()

    class Meta:
        verbose_name = 'цитата'
        verbose_name_plural = 'цитаты'
        default_related_name = 'quotes'
        ordering = ('-creation_date',)

    def __str__(self):
        return f'Цитата {self.user}'
