# Generated by Django 3.2 on 2023-05-14 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Биография'),
        ),
    ]
