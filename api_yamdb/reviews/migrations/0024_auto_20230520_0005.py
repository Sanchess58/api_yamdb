# Generated by Django 3.2 on 2023-05-19 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0023_alter_title_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Слаг категории'),
        ),
    ]
