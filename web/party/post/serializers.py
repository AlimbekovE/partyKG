from rest_framework.serializers import ModelSerializer

from party.account.serializers import UserProfileSerializer
from party.post.models import Post, PostImages


class PostImageSerializer(ModelSerializer):
    def _get_picture_url(self, obj):
        try:
            if obj.picture is None:
                return None

            url = obj.picture.url
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        except:
            return ''

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['picture'] = self._get_picture_url(instance)
        return res

    class Meta:
        model = PostImages
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['owner'] = UserProfileSerializer(instance.owner).data
        return representation
