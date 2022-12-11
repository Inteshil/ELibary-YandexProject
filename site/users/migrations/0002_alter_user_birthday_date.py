# Generated by Django 3.2.16 on 2022-12-11 18:06

from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday_date',
            field=models.DateField(blank=True, null=True, validators=[users.validators.birthday_date_validator], verbose_name='день рождения'),
        ),
    ]
