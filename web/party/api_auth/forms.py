from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import exceptions

from party.core.utils import normalize_phone
from party.api_auth.utils import authenticate_user
from party.core.forms import APIForm
from party.core.validators import validate_phone, validate_code

User = get_user_model()


class LoginForm(APIForm):
    phone = forms.CharField(min_length=3, max_length=32, validators=[validate_phone])
    password = forms.CharField(min_length=6, max_length=128)

    def api_method(self):
        return authenticate_user(phone=self.cleaned_data['phone'], password=self.cleaned_data['password'])

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone = normalize_phone(phone)
        if not User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(_('User with phone number {phone} does not exist').format(phone=phone))

        return phone


class ActivateAccountForm(APIForm):
    phone = forms.CharField(required=True)
    code = forms.CharField(required=True, validators=[validate_code])

    def clean(self):
        cleaned_data = super().clean()
        User = get_user_model()
        phone = cleaned_data.get('phone', '')
        if not phone:
            raise forms.ValidationError(_('Please, provide phone number'))
        cleaned_data['phone'] = normalize_phone(phone)
        code = cleaned_data.get('code', '')
        if not code or not User.objects.filter(phone=phone, activation_code=code, is_active=False).exists():
            raise forms.ValidationError(_('Account not found'))
        return cleaned_data

    def api_method(self, *args, **kwargs):
        User = get_user_model()
        user = User.objects.filter(activation_code=self.cleaned_data['code'], is_active=False).last()
        user.activate_with_code(self.cleaned_data['code'])
        return user


class ResendActivationForm(APIForm):
    phone = forms.CharField(min_length=9, max_length=32)

    def clean_phone(self):
        User = get_user_model()
        phone = normalize_phone(self.cleaned_data['phone'])
        if not User.objects.filter(phone=phone, is_active=False).exists():
            raise forms.ValidationError(_('Account not found'))
        return phone

    def api_method(self, *args, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(phone=self.cleaned_data['phone'], is_active=False)
        except User.DoesNotExist:
            raise exceptions.NotFound(_('Account not found'))
        user.activation_code = user.create_activation_code()
        user.save(is_sms_activation=True)
        return user.activation_code
