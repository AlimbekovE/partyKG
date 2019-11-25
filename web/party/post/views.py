from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from party.core.permissions import IsOwnerOrIsAdmin, IsAdmin
from party.post.models import Post
from party.post.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsOwnerOrIsAdmin]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['owner'] = request.user.id

        serializer = self.get_serializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
