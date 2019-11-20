import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = {
    'debug.debug': 'true' == os.environ.get('DJ_DEBUG', False),

    'general.static_root': os.environ.get('DJ_STATIC_ROOT', os.path.join(BASE_DIR, 'static/')),
    'general.media_root': os.environ.get('DJ_MEDIA_ROOT', os.path.join(BASE_DIR, 'media/')),

    'security.allowed_hosts': os.environ.get('DJ_ALLOWED_HOSTS', '*'),
    'security.secret_key': os.environ.get('DJ_LOG_SECRET', '34!zz@r4nyi2p3phki^2e^f3vx5u2#tda6#uz%9%v7=7#10gi0'),
    'database.name': os.environ.get('POSTGRES_DB', 'postgres'),
    'database.user': os.environ.get('POSTGRES_USER', 'postgres'),
    'database.password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
    'database.host': os.environ.get('POSTGRES_HOST', 'postgres'),
    'database.port': os.environ.get('POSTGRES_PORT', 5432),
    'language.language_code': os.environ.get('DJ_LANGUAGE_CODE', 'ru-ru')
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['security.secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/usr/src/app/static"

MEDIA_ROOT = config['general.media_root']
MEDIA_URL = '/media/'
