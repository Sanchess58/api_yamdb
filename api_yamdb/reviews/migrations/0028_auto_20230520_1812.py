# Generated by Django 3.2 on 2023-05-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0027_rename_genres_title_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genres',
            field=models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='Жанры'),
        ),
    ]
