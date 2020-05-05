import os
from party.core.utils import PRODUCTION_ENV

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'party')

config = {
    'debug.debug': 'true' == os.environ.get('DJ_DEBUG', False),
    'env.name': os.environ.get('ENV', PRODUCTION_ENV),

    'general.static_root': os.environ.get('DJ_STATIC_ROOT', os.path.join(BASE_DIR, 'static/')),
    'general.media_root': os.environ.get('DJ_MEDIA_ROOT', os.path.join(BASE_DIR, 'media/')),

    'security.allowed_hosts': os.environ.get('DJ_ALLOWED_HOSTS', '*'),
    'security.secret_key': os.environ.get('DJ_LOG_SECRET', '34!zz@r4nyi2p3phki^2e^f3vx5u2#tda6#uz%9%v7=7#10gi0'),
    'database.name': os.environ.get('POSTGRES_DB', 'postgres'),
    'database.user': os.environ.get('POSTGRES_USER', 'postgres'),
    'database.password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
    'database.host': os.environ.get('POSTGRES_HOST', 'postgres'),
    'database.port': os.environ.get('POSTGRES_PORT', 5432),
    'language.language_code': os.environ.get('DJ_LANGUAGE_CODE', 'ru-ru'),

    'sms.backend': os.environ.get('DJ_SMS_BACKEND', ''),
    'sms.username': os.environ.get('DJ_SMS_USERNAME', ''),
    'sms.password': os.environ.get('DJ_SMS_PASSWORD', ''),
    'sms.sender_name': os.environ.get('DJ_SMS_SENDER_NAME', ''),
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['security.secret_key']
ENV = config['env.name']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['debug.debug']

ALLOWED_HOSTS = config['security.allowed_hosts'].split(',')

SEND_SMS_BACKEND = f"sms_sender.backends.{config['sms.backend']}"
SMS_LOGIN = config['sms.username']
SMS_PASSWORD = config['sms.password']
SMS_SENDER_NAME = config['sms.sender_name']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',

    'import_export',
    'debug_toolbar',

    'party.account',
    'party.api_auth',
    'party.post',
    'party.event',
    'party.locations',
    'party.vote',
    'party.core',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'party.core.paginators.CustomPagination',
    'PAGE_SIZE': 50,

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'party.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'party.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config['database.name'],
        'USER': config['database.user'],
        'PASSWORD': config['database.password'],
        'HOST': config['database.host'],
        'PORT': config['database.port'],
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            },
        },
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'WARNING'),
            },
        },
    }

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

AUTH_USER_MODEL = 'account.User'

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/usr/src/app/static'

MEDIA_ROOT = config['general.media_root']
MEDIA_URL = '/media/'

LOCALE_PATHS = (
    os.path.join(SRC_DIR, 'locale'),
)

# Import/Export Configs https://django-import-export.readthedocs.io/en/latest/
IMPORT_EXPORT_USE_TRANSACTIONS = True

INTERNAL_IPS = ['127.0.0.1', '172.17.0.1', 'localhost']

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}