from rest_framework import serializers

from party.account.serializers import UserSerializer
from party.event.models import Event, EventDiscussion


class EventSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(format='%d-%m-%Y %H:%M', input_formats=['%d-%m-%Y %H:%M', 'iso-8601'])

    class Meta:
        model = Event
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = UserSerializer(instance.owner).data
        return representation


class CustomListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        calendar = {}
        for item in data:
            item = self.child.to_representation(item)
            day, event_time = item

            if day in calendar:
                calendar[day].append(event_time)
            else:
                calendar[day] = [event_time]
        return calendar

    @property
    def data(self):
        return self.to_representation(self.instance)


class EventListSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format='%H:%M', source='datetime')

    class Meta:
        model = Event
        exclude = ['datetime']
        list_serializer_class = CustomListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = UserSerializer(instance.owner).data
        return instance.datetime.day, representation


class EventDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDiscussion
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['title'] = instance.event.title
        representation['description'] = instance.event.description
        representation['user'] = UserSerializer(instance.user, context=self.context).data
        return representation
