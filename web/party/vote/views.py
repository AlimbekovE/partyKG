from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from party.core.permissions import IsObjectUserOrReadOnly, IsObjectOwnerOrReadOnly
from party.vote.models import Question, Vote
from party.vote.serializers import QuestionSerializer, VoteSerializer


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


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsObjectUserOrReadOnly))
def vote(request):
    answer = request.data.get('answer')
    question = request.data.get('question')
    Vote.objects.update_or_create(user=request.user, question_id=question, defaults={'answer': answer})
    return Response(status=200)
