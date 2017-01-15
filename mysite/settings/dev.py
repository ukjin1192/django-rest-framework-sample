#!usr/bin/python
# -*- coding:utf-8 -*-

from base import *

DEBUG = True
ALLOWED_HOSTS = [
    '*',
]
INTERNAL_IPS = (
    '192.168.99.100',
    '127.0.0.1',
)

# CORS(Cross-Origin Resource Sharing) settings
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.get('django', 'project_name'),
        'USER': 'root',
        'PASSWORD': config.get('mysql:development', 'password'),
        'HOST': '',
        'PORT': '',
        'DEFAULT-CHARACTER-SET': 'utf8',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Use django-silk as live profiling and inspection tool
RUN_SILK = DEBUG

if RUN_SILK:

    MIDDLEWARE = ['silk.middleware.SilkyMiddleware', ] + MIDDLEWARE

    INSTALLED_APPS += (
        'silk',
    )
