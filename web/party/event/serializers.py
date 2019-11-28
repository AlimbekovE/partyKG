from rest_framework import serializers

from party.account.serializers import UserProfileSerializer
from party.event.models import Event


class EventSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format='%d-%m-%Y %H:%M', input_formats=['%d-%m-%Y %H:%M', 'iso-8601'])

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = UserProfileSerializer(instance.owner).data
        return representation


class EventListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%H:%M', source='datetime')

    class Meta:
        model = Event
        exclude = ['datetime']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = UserProfileSerializer(instance.owner).data
        return {instance.datetime.day: representation}
