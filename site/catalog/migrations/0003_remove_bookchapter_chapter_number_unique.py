# Generated by Django 3.2.16 on 2022-12-20 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20221220_1924'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='bookchapter',
            name='chapter_number_unique',
        ),
    ]
