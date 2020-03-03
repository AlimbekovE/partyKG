# Generated by Django 2.2 on 2020-03-03 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20191231_0415'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-created', '-id'), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ('-created',), 'verbose_name': 'комментарий к посту', 'verbose_name_plural': 'комментарии к посту'},
        ),
        migrations.AlterModelOptions(
            name='postimages',
            options={'ordering': ('created',), 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Владелец поста'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заглавие'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='message',
            field=models.TextField(blank=True, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.Post', verbose_name='пост'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
