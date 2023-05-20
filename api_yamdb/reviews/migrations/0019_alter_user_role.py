# Generated by Django 3.2 on 2023-05-19 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0018_merge_0003_auto_20220120_0209_0017_alter_title_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'admin'), ('moderator', 'moderator')], default='user', help_text='Выберете роль пользователя', max_length=20, verbose_name='Роль'),
        ),
    ]
