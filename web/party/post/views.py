from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes

from party.core.paginators import CustomPagination
from party.core.permissions import IsOwnerOrIsAdmin, IsAdmin, IsPostImageOwnerOrAdmin, \
    IsObjectUserOrReadOnly
from party.post.models import Post, PostImages, PostComment, PostFavorite

from party.post.serializers import PostSerializer, PostImageSerializer, PostCommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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

    @action(methods=['GET'], detail=True)
    def comments(self, request, pk, *args, **kwargs):
        self.pagination_class = CustomPagination
        self.pagination_class.page_size = 50

        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.select_related('user')
        page = self.paginate_queryset(comments)

        if page is not None:
            serializers = PostCommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializers.data)
        serializers = PostCommentSerializer(comments, many=True)
        return Response(serializers.data)


class PostImagesViewsSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = PostImageSerializer
    queryset = PostImages.objects.select_related('post')
    pagination_class = None

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permission_classes = [IsPostImageOwnerOrAdmin]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class PostCommentViewSet(mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsObjectUserOrReadOnly,)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = PostCommentSerializer(data=data, context={'request': self.request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_favorite(request):
    post_id = request.data.get('post_id')
    make_favorite = request.data.get('make_favorite')
    if make_favorite == 'true':
        PostFavorite.objects.get_or_create(user=request.user, post_id=post_id)
    elif make_favorite == 'false':
        PostFavorite.objects.filter(user=request.user, post_id=post_id).delete()
    return Response(status=200)
