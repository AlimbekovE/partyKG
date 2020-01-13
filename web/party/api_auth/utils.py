from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from rest_framework import exceptions
from django.utils.translation import gettext as _
from sms_sender import send_sms

from party.core.utils import PRODUCTION_ENV


def authenticate_user(phone, password):
    User = get_user_model()

    user = User.objects.filter(phone=phone)

    if not user.exists():
        raise exceptions.NotFound(_('Account not found.'))
    if not user.first().check_password(password):
        raise exceptions.AuthenticationFailed()
    user = authenticate(phone=phone, password=password)
    if not user or not user.is_active:
        raise exceptions.PermissionDenied()

    token = user.get_token()
    return user, token.key


def send_sms_account_verification(phone, code):

    message = f'Код активации: {code}'
    try:
        if settings.ENV == PRODUCTION_ENV:
            send_sms(phone, message)
    except:
        pass
