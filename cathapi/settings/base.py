"""
Django settings for cathapi project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import logging.config  # pylint: disable=C0413,C0411
import os

from django.core.management.utils import get_random_secret_key

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.abspath(__file__ + '/../../../')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = None
secret_files = []
for secret_dir in [BASE_DIR, '/etc']:
    secret_file = os.path.join(secret_dir, 'secret_key.txt')
    try:
        with open(secret_file) as f:
            SECRET_KEY = f.read().strip()
    except FileNotFoundError:
        secret_files.extend([secret_file])
        continue

if not SECRET_KEY:
    SECRET_KEY = get_random_secret_key()
    # raise FileNotFoundError(
    #     'failed to get SECRET_KEY from local file, tried: {}'.format(", ".join(secret_files)))



del secret_files

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["api01.cathdb.info", ".cathdb.info", "orengoapi01", "localhost",
                 "127.0.0.1", "127.0.0.1:8000", "0.0.0.0", "192.168.99.1", "131.152.84.4", "172.17.0.1", "192.168.122.1"]

# SENTRY (logging)

sentry_sdk.init(
    dsn="https://09c10478769d49959a287589b3183f2a@sentry.io/1308416",
    integrations=[DjangoIntegration()]
)

# CELERY

BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/London'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "cathapi"
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

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
    'cathapi',
    'select_template_api',
    'frontend',
    'corsheaders',
    'drf_yasg',
    'django_extensions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cathapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'cathapi.wsgi.application'

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://localhost:8000',
    'http://orengoapi01:8000',
    'http://api01.cathdb.info',
    'https://expasy.org',
)

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# see environment settings

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

REACT_APP_DIR = os.path.join(BASE_DIR, 'frontend')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, 'build', 'static'),
]

# REST framework

REST_FRAMEWORK = {
    # User Django's standard `django.contrib.auth` permissions,
    # or allow read-only for unauthenticated users
    'DEFAULT_PERMISSION_CLASSES': (
        # TODO: sort out default permissions on new API users
        #       (or add them to 'API' Group) so we can use
        #       model permissions
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication', ),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'api_key': {
            'type': 'apiKey',
            'name': 'api_key',
            'in': 'header'
        }
    }
}

# logging
# https://docs.djangoproject.com/en/2.1/topics/logging/
# https://lincolnloop.com/blog/django-logging-right-way/


LOGGING_CONFIG = None
LOG_LEVEL = os.environ.get('CATHAPI_LOGLEVEL', 'info').upper()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)35s:%(lineno)-5s %(levelname)-8s | %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'celery': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'celery.log',
            'formatter': 'console',
            'maxBytes': 1024 * 1024 * 100,  # 100 mb
        },
        # this causes permission problems with production server so
        # log via stdout/stderr and let web server deal with issues
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': 'debug.log',
        # },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True,
        },
        'cathapi': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
        'cathpy': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
        'frontend': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
        'select_template_api': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            'propagate': True,
        },
        'celery': {
            'level': LOG_LEVEL,
            'handlers': ['celery', 'console'],
            'level': 'DEBUG',
        },
    }
})
