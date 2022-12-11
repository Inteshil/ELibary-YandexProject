from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse

from users.models import User
from catalog.managers import BookManager


AGE_RATING_CHOICES = (
    ('0+', '0+'),
    ('6+', '6+'),
    ('12+', '12+'),
    ('16+', '16+'),
    ('18+', '18+'),
)


class Book(models.Model):
    name = models.CharField('название', max_length=100)
    content = models.FileField(
        'содержимое', upload_to='books/%Y/%m',
        validators=[FileExtensionValidator(['pdf', 'fb2'])]
        )
    preview = models.ImageField('превью', upload_to='previews/%Y/%m')
    is_published = models.BooleanField('опубликовано', default=True)
    is_blocked = models.BooleanField('заблокировано', default=False)
    description = models.TextField(
        'описание', max_length=3000, default='Без описания'
        )
    slug = models.SlugField('slug', max_length=100)
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
        return reverse('catalog:book_detail', kwargs={'pk': self.pk})


class Tag(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        default_related_name = 'tags'

    def __str__(self):
        return self.name
