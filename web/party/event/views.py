from rest_framework import mixins, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from party.core.paginators import CustomPagination
from party.core.permissions import IsOwnerOrIsAdmin, IsAdmin, IsObjectUserOrReadOnly
from party.event.models import Event
from party.event.serializers import EventSerializer, EventListSerializer, EventDiscussionSerializer
from party.event.permissions import IsAdminOrbjectIsPersonal


class EventViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.filter(is_personal=False)
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrbjectIsPersonal, IsAuthenticated]
    pagination_class = CustomPagination
    pagination_class.size = 31


    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        month = self.request.GET.get('month', None)
        year = self.request.GET.get('year', None)
        is_personal = self.request.GET.get('is_personal', False)

        qs = super().get_queryset()
        if month and year:
            qs = qs.filter(
                datetime__month=month,
                datetime__year=year,
                is_personal=bool(is_personal),
            )
        elif is_personal:
            qs = Event.objects.filter(
                datetime__month=month,
                datetime__year=year,
                is_personal=bool(is_personal),
                owner=self.request.user
            )
        return qs

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id

        serializer = self.get_serializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def discussions(self, request, pk, *args, **kwargs):
        self.pagination_class = CustomPagination
        self.pagination_class.page_size = 10

        question = get_object_or_404(Event, pk=pk)
        discussions = question.discussions.select_related('user')
        page = self.paginate_queryset(discussions)

        if page is not None:
            serializers = EventDiscussionSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializers.data)
        serializers = EventDiscussionSerializer(discussions, many=True)
        return Response(serializers.data)


class EventDiscussionsViewSet(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    queryset = Event.objects.filter(is_personal=False)
    serializer_class = EventDiscussionSerializer
    permission_classes = (IsObjectUserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = EventDiscussionSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
