"""
Django settings for easy_flat project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import datetime
import rest_framework_jwt
import os
import environ
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
env_file = os.path.join(os.path.dirname(Path(__file__).resolve(strict=True).parent), '.env')
env = environ.Env()
environ.Env.read_env(env_file=env_file)
def get_env_value(name: str, default: any = None):
    return env(name, default=None) or os.environ.get(name) or default

# Build paths inside the project like this: BASE_DIR / 'subdir'.
AUTH_USER_MODEL = 'user.CustomUser'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ozt*m_xsdde&eh!5_q^&tgkw)5d7@n)lhj&a^tri*(eqfwt$%l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_jwt',
    'django_filters',
    'community',
    'user',
    'api',
    'flat'
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

ROOT_URLCONF = 'easy_flat.urls'

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

WSGI_APPLICATION = 'easy_flat.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': get_env_value('ENGINE',default='django.db.backends.postgresql'),
        'NAME': get_env_value('NAME_DB',default='NAME_DB'),
        'USER': get_env_value('USER_DB',default='USER_DB'),
        'PASSWORD': get_env_value('PASSWORD_DB',default='PASSWORD_DB'),
        'HOST': get_env_value('HOST_DB',default='127.0.0.1'),
        'PORT': get_env_value('PORT_DB',default=5432)
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 24 * 365),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(seconds=60 * 60 * 24 * 365),
}
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'paveligin1861@gmail.com'
EMAIL_HOST_PASSWORD = 'qazwsx1861'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
FRONTEND_URL = 'http://127.0.0.1:8000/'
