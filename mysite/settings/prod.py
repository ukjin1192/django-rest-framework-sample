#!usr/bin/python
# -*- coding:utf-8 -*-

from base import *

DEBUG = False
ALLOWED_HOSTS = [
    config.get('django', 'domain_name'),
]

# CORS(Cross-Origin Resource Sharing) settings
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    '*.' + config.get('django', 'domain_name') ,
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.get('django', 'project_name'),
        'USER': 'root',
        'PASSWORD': config.get('mysql:production', 'password'),
        'HOST': config.get('mysql:production', 'end_point'),
        'PORT': '3306',
        'DEFAULT-CHARACTER-SET': 'utf8',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config.get('redis:production', 'end_point'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

RUN_SILK = False
