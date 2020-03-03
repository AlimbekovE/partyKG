from django.contrib.auth import get_user_model
from django.db import models

from django.utils.translation import gettext as _
from party.post.utils import FILE_TYPE

User = get_user_model()


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='posts', null=True,
                              verbose_name=_('post owner'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created', '-id')
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def is_favorited(self, request):
        if request.user.is_authenticated:
            return self.favorites.filter(user=request.user).exists()
        return False


class PostImages(models.Model):
    def user_directory_path(instance, filename):
        return f'posts/{instance.post.id}/images/{filename}'

    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(choices=FILE_TYPE, max_length=50, default='image')

    def __str__(self):
        return f'фото {self.get_type_display()} к {self.post}'

    class Meta:
        ordering = ('created',)
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class PostFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ('-created',)


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',
                             on_delete=models.CASCADE, verbose_name=_('post'))
    user = models.ForeignKey(User, related_name='comments',
                             on_delete=models.CASCADE, verbose_name=_('user'))
    message = models.TextField(blank=True, verbose_name=_('message'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))

    def __str__(self):
        return f'комментариы к посту {self.post}'

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Post comment')
        verbose_name_plural = _('Post comments')
