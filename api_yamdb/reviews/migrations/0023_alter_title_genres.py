# Generated by Django 3.2 on 2023-05-19 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0022_auto_20230519_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genres',
            field=models.ManyToManyField(related_name='titles', to='reviews.Genre', verbose_name='Жанры'),
        ),
    ]
