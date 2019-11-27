from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField()
    number_of_people = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    datetime = models.DateTimeField()
