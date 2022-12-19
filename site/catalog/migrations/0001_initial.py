# Generated by Django 3.2.16 on 2022-12-19 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_created=True, auto_now_add=True, verbose_name='дата создания')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('preview', models.ImageField(upload_to='previews/%Y/%m', verbose_name='превью')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликовано')),
                ('is_blocked', models.BooleanField(default=False, verbose_name='заблокировано')),
                ('description', models.TextField(default='Без описания', max_length=3000, verbose_name='описание')),
                ('age_rating', models.SmallIntegerField(choices=[(0, 'Отсутствует'), (1, '16+'), (2, '18+')], default='нет', verbose_name='возрастной рейтинг')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'книга',
                'verbose_name_plural': 'книги',
                'default_related_name': 'books',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
                'default_related_name': 'tags',
            },
        ),
        migrations.CreateModel(
            name='BookComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_datetime', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='дата и время создания отзыва')),
                ('text', models.TextField(max_length=100000, verbose_name='текст отзыва')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book', verbose_name='книга отзыва')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор отзыва')),
            ],
            options={
                'verbose_name': 'отзыв',
                'verbose_name_plural': 'отзывы',
            },
        ),
        migrations.CreateModel(
            name='BookChapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('number', models.PositiveIntegerField(verbose_name='порядковый номер')),
                ('is_published', models.BooleanField(default=True, verbose_name='опубликовано')),
                ('content', models.TextField(max_length=100000, verbose_name='содержание')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='catalog.book', verbose_name='книга')),
            ],
            options={
                'verbose_name': 'глава',
                'verbose_name_plural': 'главы',
                'default_related_name': 'chapters',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='books', to='catalog.Tag', verbose_name='теги'),
        ),
        migrations.AddConstraint(
            model_name='bookchapter',
            constraint=models.UniqueConstraint(fields=('book', 'number'), name='chapter_number_unique'),
        ),
    ]
