from django.db import models
from django.urls import reverse

from users.models import User
from catalog.managers import BookManager, BookChapterManager


AGE_RATING_CHOICES = (
    ('0+', '0+'),
    ('6+', '6+'),
    ('12+', '12+'),
    ('16+', '16+'),
    ('18+', '18+'),
)


class Book(models.Model):
    name = models.CharField('название', max_length=100)
    preview = models.ImageField('превью', upload_to='previews/%Y/%m')
    is_published = models.BooleanField('опубликовано', default=True)
    is_blocked = models.BooleanField('заблокировано', default=False)
    description = models.TextField(
        'описание', max_length=3000, default='Без описания'
        )
    age_rating = models.TextField(
        'возрастной рейтинг', choices=AGE_RATING_CHOICES, null=True, blank=True
        )
    creation_data = models.DateField(
        'дата создания', auto_created=True, auto_now_add=True
        )
    tags = models.ManyToManyField('Tag')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = BookManager()

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'
        default_related_name = 'books'

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

    def get_neighboring_chapters(self):
        previous = BookChapter.objects.published().filter(
            number__lt=self.number
            ).last()
        next = BookChapter.objects.published().filter(
            number__gt=self.number
            ).first()
        return {'previous': previous, 'next': next}


class Tag(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        default_related_name = 'tags'

    def __str__(self):
        return self.name
