from django.db import models
from django.contrib.auth import get_user_model

from party.vote.utils import ANSWER

User = get_user_model()


class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=200)
    project_date = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    answer = models.CharField(choices=ANSWER, max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')

    class Meta:
        unique_together = ('user', 'question')
