"""
Django settings for Sushiapi project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""


import os
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u4bp7^p&0=7$jinz_gekgxp=00nks3_4wueyyn3!h+f80+e5kj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tuerca6.ing.puc.cl']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'masterapp',
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

ROOT_URLCONF = 'Sushiapi.urls'

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

WSGI_APPLICATION = 'Sushiapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_BEAT_SCHEDULE = {
    'pedir_productos_propios': {
        'task': 'masterapp.tasks.pedir_productos_propios',
        'schedule': crontab(minute='*/15')  # execute every minute
    },
    'pedir_productos_ajenos': {
        'task': 'masterapp.tasks.pedir_productos_ajenos',
        'schedule': crontab(minute='*/3')  # execute every minute
    },
    'fabricar_productos_propios': {
        'task': 'masterapp.tasks.fabricar_productos_propios',
        'schedule': crontab(minute='*/5')  # execute every minute
    },
    'fabricar_productos_intermedios': {
        'task': 'masterapp.tasks.fabricar_productos_intermedios',
        'schedule': crontab(minute='*/5')  # execute every minute
    },
    'vaciar_despacho': {
        'task': 'masterapp.tasks.vaciar_despacho',
        'schedule': crontab(minute=0, hour='*/6')  # execute every minute
    },
    'manejar_pedidos_cliente': {
        'task': 'masterapp.tasks.manejar_pedidos_cliente',
        'schedule': crontab(minute='*/8')  # execute every minute
    },
    'vaciar_pulmon': {
        'task': 'masterapp.tasks.vaciar_pulmon',
        'schedule': crontab(minute='*/6')  # execute every minute
    },
    'pedir_azucar': {
        'task': 'masterapp.tasks.pedir_azucar',
        'schedule': crontab(minute='*/60')  # execute every minute
    },
    'vaciar_recepcion': {
        'task': 'masterapp.tasks.vaciar_recepcion',
        'schedule': crontab(minute='*/20')  # execute every minute
    },
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
