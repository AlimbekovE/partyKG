from django.contrib.auth import get_user_model
from rest_framework import serializers

from party.core.utils import normalize_phone

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = (
            'name', 'surname', 'patronymic',
            'phone', 'email', 'password'
        )

    def validate_phone(self, value):
        value = normalize_phone(value)
        return value

    def create(self, validated_data):
        instance = User.create(validated_data.pop('phone'), validated_data.pop('password'), is_sms_activated=True)
        return instance
