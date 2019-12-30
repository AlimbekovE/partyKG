from django.contrib.auth import get_user_model
from django.db import models

from party.post.utils import FILE_TYPE

User = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', '-id')


class PostImages(models.Model):
    def user_directory_path(instance, filename):
        return f'posts/{instance.post.id}/images/{filename}'

    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=FILE_TYPE, max_length=50, default='image')

    class Meta:
        ordering = ['created']
