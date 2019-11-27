from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from party.event.models import Event
from party.event.serializers import EventSerializer


class EventViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)

        qs = super().get_queryset()
        if month and year:
            qs = qs.filter(datetime__month=month, datetime__year=year)
        return qs

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id

        serializer = self.get_serializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
