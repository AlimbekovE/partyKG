from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _

User = get_user_model()


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    number_of_people = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    is_personal = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['datetime']

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
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ManyToManyField(User)
    date = models.DateTimeField(auto_now_add=True)


class EventDiscussion(models.Model):
    event = models.ForeignKey(Event, related_name='discussions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='event_discussions', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

