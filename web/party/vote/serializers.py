from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from party.account.serializers import UserSerializer
from party.vote.models import Question, Vote, QuestionDiscussion
from django.db.models import Q, Count


class QuestionSerializer(ModelSerializer):
    project_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M', input_formats=['%d-%m-%Y %H:%M', 'iso-8601'])

    class Meta:
        model = Question
        fields = '__all__'

    @staticmethod
    def _get_percent(count, total_count):
        if count != 0 or total_count != 0:
            percent = count / (total_count / 100)
            return round(percent, 1)
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        counts = Question.objects.aggregate(
            total_count=Count('votes'),
            behind_count=Count('votes', filter=Q(votes__answer='behind')),
            against_count=Count('votes', filter=Q(votes__answer='against')),
            abstain_count=Count('votes', filter=Q(votes__answer='abstain')),
        )
        representation['behind'] = {
            'percent': self._get_percent(counts['behind_count'], counts['total_count']),
            'count': counts['behind_count']
        }
        representation['against'] = {
            'percent': self._get_percent(counts['against_count'], counts['total_count']),
            'count': counts['against_count']
        }
        representation['abstain'] = {
            'percent': self._get_percent(counts['abstain_count'], counts['total_count']),
            'count': counts['abstain_count']
        }
        representation['total_count'] = counts['total_count']
        return representation


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class QuestionDiscussionSerializer(ModelSerializer):
    class Meta:
        model = QuestionDiscussion
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['title'] = instance.question.title
        representation['question'] = instance.question.question_text
        representation['user'] = UserSerializer(instance.user, context=self.context).data
        return representation
