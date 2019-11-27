from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    number_of_people = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    datetime = models.DateTimeField()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['datetime']
