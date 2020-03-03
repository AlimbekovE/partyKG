from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from party.vote.utils import ANSWER

User = get_user_model()


class Question(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='questions', verbose_name=_('owner'))
    question_text = models.TextField(verbose_name=_('question text'))
    project_date = models.DateTimeField(verbose_name=_('project date'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created date'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='votes', verbose_name=_('user'))
    answer = models.CharField(choices=ANSWER, max_length=100, verbose_name=_('answer'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 related_name='votes', verbose_name=_('question'))

    def __str__(self):
        return f'ответ на вопрос {self.question} от {self.user}'

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')


class QuestionDiscussion(models.Model):
    question = models.ForeignKey(Question, related_name='discussions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='question_discussions', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'обсуждение вопроса {self.question}'

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Question Discussion')
        verbose_name_plural = _('Question Discussions')
