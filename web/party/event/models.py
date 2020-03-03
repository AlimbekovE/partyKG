from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _

User = get_user_model()


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name=_('event owner'))
    title = models.CharField(max_length=255, null=True, blank=True,
                             verbose_name=_('title'))
    description = models.TextField(null=True, blank=True,
                                   verbose_name=_('description'))
    number_of_people = models.PositiveIntegerField(null=True, blank=True,
                                                   verbose_name=_('number_of_people'))
    location = models.CharField(max_length=255, verbose_name=_('location'))
    datetime = models.DateTimeField(verbose_name=_('datetime'))
    is_personal = models.BooleanField(default=False, null=True, blank=True,
                                      verbose_name=_('is_personal?'))

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ('datetime',)

    def get_qr_code_url(self, request=None):
        if self.pk:
            url = reverse('qr_code', kwargs={'pk': self.pk})
            if request:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def get_user_visit_url(self):
        if self.pk:
            return reverse('event_visits_list', kwargs={'pk': self.pk})
        return ''


class Participant(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE,
                                 related_name='participants', verbose_name=_('event'))
    user = models.ManyToManyField(User, verbose_name=_('user'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('date'))

    def __str__(self):
        return f'участник {self.user}'

    class Meta:
        ordering = ('-date',)
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')


class EventDiscussion(models.Model):
    event = models.ForeignKey(Event, related_name='discussions',
                              on_delete=models.CASCADE, verbose_name=_('event'))
    user = models.ForeignKey(User, related_name='event_discussions',
                             on_delete=models.CASCADE, verbose_name=_('user'))
    message = models.TextField(blank=True, verbose_name=_('message'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))

    def __str__(self):
        return f'дискуссия k {self.event}'

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Event discussion')
        verbose_name_plural = _('Event discussions')
