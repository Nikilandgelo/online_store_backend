import os
from pathlib import Path
from dotenv import load_dotenv
import socket


# WITH VPN WITHOUT IT EMAIL SENDING NOT WORKING, BECAUSE VPN ADDING TO DNS HOSTNAME SOME DOTS AT THE END
socket.getfqdn = lambda name='': 'localhost'

load_dotenv(override=True)

BASE_DIR: Path = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS: list = []

DATABASES: dict = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

DEBUG: bool = True

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'Adress',
    'Categories',
    'Order',
    'Parameter',
    'Product',
    'Shop',
    'ShoppingCart',
    'User',
    'django_filters',
]

LANGUAGE_CODE: str = 'en-us'

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'graduate_work.middlewares.EmailConfirmationMiddleware',
]

ROOT_URLCONF: str  = 'graduate_work.urls'

SECRET_KEY: str | None = os.getenv('SECRET_KEY')

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

TIME_ZONE: str  = 'UTC'

USE_I18N: bool = True

USE_TZ: bool = True

WSGI_APPLICATION: str = 'graduate_work.wsgi.application'


AUTH_USER_MODEL: str = 'User.User'
PASSWORD_HASHERS: list[str] = ['django.contrib.auth.hashers.BCryptSHA256PasswordHasher',]
AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


STATIC_URL: str = 'static/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

CELERY_BROKER_URL = f'redis://{os.getenv('REDIS_HOST')}:6379/0'
