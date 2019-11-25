from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from party.core.permissions import IsOwner, IsOwnerOrIsAdmin, IsAdmin
from party.post.models import Post
from party.post.serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwner]
        elif self.action in ['create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['destroy']:
            permission_classes = [IsOwnerOrIsAdmin]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {'request': self.request}
