from django.db import models
from django.urls import reverse

from catalog.managers import BookManager, BookChapterManager, CommentManager
from users.models import User


class Book(models.Model):
    AGE_RATING_CHOICES = list(enumerate(('Отсутствует', '16+', '18+')))

    name = models.CharField('название', max_length=100)
    preview = models.ImageField('превью', upload_to='previews/%Y/%m')
    is_published = models.BooleanField('опубликовано', default=True)
    is_blocked = models.BooleanField('заблокировано', default=False)
    description = models.TextField(
        'описание', max_length=3000, default='Без описания'
        )
    age_rating = models.SmallIntegerField(
        'возрастной рейтинг', choices=AGE_RATING_CHOICES, default='нет'
        )
    creation_date = models.DateField(
        'дата создания', auto_created=True, auto_now_add=True
        )
    tags = models.ManyToManyField('Tag', verbose_name='теги', blank=True)
    author = models.ForeignKey(
        User, verbose_name='автор', on_delete=models.CASCADE
        )

    objects = BookManager()

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
        default_related_name = 'books'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'book_id': self.pk})


class BookChapter(models.Model):
    name = models.CharField('название', max_length=100)
    number = models.PositiveIntegerField('порядковый номер')
    is_published = models.BooleanField('опубликовано', default=True)
    content = models.TextField('содержание', max_length=100000)
    book = models.ForeignKey(
        'Book', verbose_name='книга', on_delete=models.CASCADE
        )

    objects = BookChapterManager()

    class Meta:
        verbose_name = 'глава'
        verbose_name_plural = 'главы'
        default_related_name = 'chapters'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'catalog:book_chapter',
            kwargs={'book_id': self.book.pk, 'chapter_id': self.pk}
            )


class BookComment(models.Model):
    objects = CommentManager()

    user = models.ForeignKey(
        User,
        verbose_name='автор отзыва',
        on_delete=models.CASCADE
    )
    book = models.ForeignKey(
        Book,
        verbose_name='книга отзыва',
        on_delete=models.CASCADE
    )
    text = models.TextField('текст отзыва', max_length=100000)
    creation_datetime = models.DateTimeField(
        'дата и время создания отзыва', auto_created=True, auto_now_add=True
        )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class Tag(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        default_related_name = 'tags'

    def __str__(self):
        return self.name
