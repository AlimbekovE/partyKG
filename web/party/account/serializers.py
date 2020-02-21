from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

from party.account.models import Avatar, Position
from party.core.utils import normalize_phone
from party.locations.serializers import RegionSerializer, DistrictSerializer

User = get_user_model()

class BaseFieldSerializer():
    def get_avatar(self, obj):
        if (avatar := getattr(obj, 'avatar', None)) and \
            (image := getattr(avatar, 'image', None)):
            url = image.url
            if (request := self.context.get('request')) is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def get_position(self, obj):
        if (position := getattr(obj, 'position', None)):
            return PositionSerializer(position).data
        return position

    def get_region(self, obj):
        if (region := getattr(obj, 'region', None)):
            return RegionSerializer(region).data
        return region

    def get_district(self, obj):
        if (district := getattr(obj, 'district', None)):
            return DistrictSerializer(district).data
        return district

# serializer for login
class UserMeSerializer(serializers.ModelSerializer, BaseFieldSerializer):
    token = serializers.SerializerMethodField()
    position = serializers.SlugRelatedField(slug_field='slug', queryset=Position.objects.all())

    class Meta:
        model = User
        exclude = ('activation_code', 'password', )

    def validate_phone(self, value):
        phone = normalize_phone(value)
        if len(phone) != 12:
            raise serializers.ValidationError(_('The value is not correct phone number.'))
        return phone

    def get_token(self, obj):
        return obj.get_token().key

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['party_ticket'] = instance.party_ticket
        representation['position'] = self.get_position(instance)
        representation['avatar'] = self.get_avatar(instance)
        representation['district'] = self.get_district(instance)
        representation['region'] = self.get_region(instance)
        return representation


class UserSerializer(serializers.ModelSerializer, BaseFieldSerializer):
    date_of_birth = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y', 'iso-8601'], required=False)
    position = serializers.SlugRelatedField(slug_field='slug', queryset=Position.objects.all())

    class Meta:
        model = User
        exclude = ('is_staff', 'activation_code', 'password', )

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.send_sms_activation_code(instance.create_activation_code())
        instance.save(update_fields=['activation_code'])
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['party_ticket'] = instance.party_ticket
        representation['avatar'] = self.get_avatar(instance)
        representation['position'] = self.get_position(instance)
        representation['district'] = self.get_district(instance)
        representation['region'] = self.get_region(instance)
        return representation


class UserListSerializer(serializers.ModelSerializer, BaseFieldSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'surname', 'phone', 'position')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['avatar'] = self.get_avatar(instance)
        representation['position'] = self.get_position(instance)
        return representation


class RegisterSerializer(serializers.ModelSerializer, BaseFieldSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    date_of_birth = serializers.DateField(format='%d-%m-%Y', input_formats=['%d-%m-%Y', 'iso-8601'], required=False)
    position = serializers.SlugRelatedField(slug_field='slug', queryset=Position.objects.all())

    class Meta:
        model = User
        exclude = ('activation_code',)
        read_only_fields = ('is_staff',)

    def validate_phone(self, value):
        value = normalize_phone(value)
        return value

    def create(self, validated_data):
        instance = User.create(**validated_data, is_sms_activated=True)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['party_ticket'] = instance.party_ticket
        representation['position'] = self.get_position(instance)
        representation['district'] = self.get_district(instance)
        representation['region'] = self.get_region(instance)
        return representation


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avatar
        fields = ('id', 'user', 'image', )

    def _get_image_url(self, obj):
        try:
            if obj.image is None:
                return None

            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(url)
        except:
            return ''
        return url

    def to_representation(self, instance):
        res = super(AvatarSerializer, self).to_representation(instance)
        res['image'] = self._get_image_url(instance)
        return res


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
