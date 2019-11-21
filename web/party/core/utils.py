import re

PRODUCTION_ENV = 'production'
STAGING_ENV = 'staging'


def normalize_phone(phone):
    phone = re.sub('[^0-9+]', '', phone)
    return phone

