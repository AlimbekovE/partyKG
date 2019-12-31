from rest_framework.serializers import ModelSerializer

from party.account.serializers import UserProfileSerializer
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
        if validated_data['file'].content_type == 'image/jpeg':
            validated_data['type'] = 'image'
        else:
            validated_data['type'] = 'video'
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
        representation['owner'] = UserProfileSerializer(instance.owner).data
        return representation


class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
