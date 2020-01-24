from rest_framework.serializers import ModelSerializer

from party.account.serializers import UserSerializer
from party.post.models import Post, PostImages, PostComment


class PostImageSerializer(ModelSerializer):

    def _get_file_url(self, obj):
        if file := getattr(obj, 'file', None):
            url = file.url
            if (request := self.context.get('request')) is not None:
                return request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['file'] = self._get_file_url(instance)
        return res

    def create(self, validated_data):
        return PostImages.objects.create(**validated_data)

    class Meta:
        model = PostImages
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['files'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['owner'] = UserSerializer(instance.owner, context=self.context).data
        representation['is_favorited'] = instance.is_favorited(self.context.get('request', None))
        representation['favorites_count'] = instance.favorites.count()
        representation['comments_count'] = instance.comments.count()
        return representation


class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] =  UserSerializer(instance.user, context=self.context).data
        return representation
