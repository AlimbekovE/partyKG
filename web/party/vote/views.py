from rest_framework import status, mixins, viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action

from party.core.paginators import CustomPagination
from party.core.permissions import IsObjectUserOrReadOnly, IsObjectOwnerOrReadOnly
from party.vote.models import Question, Vote, QuestionDiscussion
from party.vote.serializers import QuestionSerializer, QuestionDiscussionSerializer, QuestionSerializerList
from party.account.models import User
from django.db.models import Q


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsObjectOwnerOrReadOnly,)

    def get_queryset(self):
        position_id = User.objects.get(pk=self.request.user.id).position
        qs = Question.objects.filter(Q(voter_position=position_id) | Q(observer_position=position_id)).distinct()
        return qs

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
        self.pagination_class.page_size = 50

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


class UserQuestionDiscussionsList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializerList

    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    pagination_class.size = 50

    def get_queryset(self):
        qs = super().get_queryset()
        is_personal = self.request.GET.get('is_personal', False)
        if is_personal:
            question_discussions = QuestionDiscussion.objects.filter(user=self.request.user)
            qs = Question.objects.filter(discussions__in=question_discussions).distinct()
        return qs
