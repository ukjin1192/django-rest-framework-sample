#!usr/bin/python
# -*- coding:utf-8 -*-

import djcelery
import os
import sys
from ConfigParser import ConfigParser
from datetime import datetime, timedelta

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT_DIR = os.path.dirname(PROJECT_DIR)
APPS_DIR = os.path.join(PROJECT_DIR, 'apps')

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, APPS_DIR)

# Get sensitive configuration
config = ConfigParser()
config.read(ROOT_DIR + '/conf/sensitive/configuration.ini')

# Application configuration
PROJECT_NAME = config.get('django', 'project_name')
ROOT_URLCONF = PROJECT_NAME + '.urls'
WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'
SECRET_KEY = config.get('django', 'secret_key')
AUTH_USER_MODEL = 'main.User'
ROOT_URLCONF = 'mysite.urls'
WSGI_APPLICATION = 'mysite.wsgi.application'
STATIC_URL = '/static/'

INSTALLED_APPS = [
    # django-suit should come before 'django.contrib.admin'
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_extensions',
    'djcelery',
    'rest_framework',
    'main',
    'utils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CorsMiddleware should come before 'CommonMiddleware'
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

# Internationalization
USE_I18N = False
TIME_ZONE = 'UTC'
USE_TZ = True

# REST framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}

# Customize return value when user requested token
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id
    }

# Customize settings for JWT(JSON Web Token)
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': jwt_response_payload_handler,
    'JWT_EXPIRATION_DELTA': timedelta(days=100)
}

# Use Celery for async tasks
djcelery.setup_loader()
BROKER_URL = 'amqp://guest:guest@localhost:5672/'       # Use RabbitMQ as broker

# Use Celery beat for cron tasks
CELERY_IMPORTS = ('utils.cron',)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
