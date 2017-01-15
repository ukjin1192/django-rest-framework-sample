#!usr/bin/python
# -*- coding: utf-8 -*-

from main.models import User
from rest_framework import serializers
from rest_framework.settings import api_settings

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'password', 'is_active', 'date_joined', 'last_login')
        # Password would not display, but required when creating an object
        extra_kwargs = {'password': {'write_only': True}, }
