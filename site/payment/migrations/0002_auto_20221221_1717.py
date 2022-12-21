# Generated by Django 3.2.16 on 2022-12-21 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_book_price'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchasedbook',
            options={'default_related_name': 'purchased'},
        ),
        migrations.AlterField(
            model_name='purchasedbook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased', to='catalog.book', verbose_name='книга'),
        ),
        migrations.AlterField(
            model_name='purchasedbook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddConstraint(
            model_name='purchasedbook',
            constraint=models.UniqueConstraint(fields=('book', 'user'), name='purchased_book_unique'),
        ),
    ]
