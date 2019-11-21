from django.conf import settings
from sms_sender import send_sms

from party.core.utils import PRODUCTION_ENV


def send_sms_account_verification(phone, code):

    message = f'Код активации: {code}'
    try:
        if settings.ENV == PRODUCTION_ENV:
            send_sms(phone, message)
    except:
        pass
