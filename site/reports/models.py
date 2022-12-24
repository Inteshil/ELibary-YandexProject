from django.db import models

from users.models import User
from catalog.models import Book


class BookReport(models.Model):
    REASON_CHOICES = (
        (0, 'Другое'),
        (1, 'Пропаганда запрещенных веществ'),
        (2, 'Пропаганда ЛГБТ'),
        (3, 'Несоответсвие возрастному рейтингу'),
        (4, 'Разжигание вражды и ненависти'),
        (5, 'Нарушение авторского права'),
        (6, 'Нарушение правил сайта'),
    )

    sender = models.ForeignKey(
        User, verbose_name='отправитель', on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book, verbose_name='книга', on_delete=models.CASCADE
    )
    reason = models.SmallIntegerField(
        'причина', choices=REASON_CHOICES, default=0
    )
    content = models.CharField('объяснение', max_length=5000)
    creation_datetime = models.DateTimeField(
        'дата и время создания', auto_now_add=True
    )

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

    def __str__(self):
        return f'Жалоба пользователя {self.sender}'
