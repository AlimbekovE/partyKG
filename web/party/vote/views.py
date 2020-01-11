from rest_framework import status, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action

from party.core.paginators import CustomPagination
from party.core.permissions import IsObjectUserOrReadOnly, IsObjectOwnerOrReadOnly
from party.vote.models import Question, Vote
from party.vote.serializers import QuestionSerializer, QuestionDiscussionSerializer


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsObjectOwnerOrReadOnly,)

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True)
    def discussions(self, request, pk, *args, **kwargs):
        self.pagination_class = CustomPagination
        self.pagination_class.page_size = 10

        question = get_object_or_404(Question, pk=pk)
        discussions = question.discussions.select_related('user')
        page = self.paginate_queryset(discussions)

        if page is not None:
            serializers = QuestionDiscussionSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializers.data)
        serializers = QuestionDiscussionSerializer(discussions, many=True)
        return Response(serializers.data)


class QuestionDiscussionsViewSet(mixins.CreateModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionDiscussionSerializer
    permission_classes = (IsObjectUserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = QuestionDiscussionSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsObjectUserOrReadOnly))
def vote(request):
    answer = request.data.get('answer')
    question = request.data.get('question')
    vote, _ = Vote.objects.update_or_create(user=request.user, question_id=question, defaults={'answer': answer})
    serializer = QuestionSerializer(vote.question)
    return Response(serializer.data, status=200)
