from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers

from party.core.utils import normalize_phone

User = get_user_model()


class UserMeSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'activation_code', 'password', )

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        instance.send_sms_activation_code(instance.create_activation_code())
        instance.save(update_fields=['activation_code'])
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'activation_code', 'password', 'is_active', 'last_login')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = (
            'name', 'surname', 'patronymic',
            'phone', 'email', 'password', 'is_staff'
        )
        read_only_fields = ('is_staff',)

    def validate_phone(self, value):
        value = normalize_phone(value)
        return value

    def create(self, validated_data):
        instance = User.create(**validated_data, is_sms_activated=True)
        return instance
