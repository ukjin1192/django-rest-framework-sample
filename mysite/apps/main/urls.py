# -*- coding: utf-8 -*-

from django.conf.urls import url
from main.views import api_root, UserViewSet

user_list = UserViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    url(
        r'^$', 
        api_root
    ),
    url(
        r'^users/$',
        user_list,
        name='user-list'
    ),
    url(
        r'^users/(?P<pk>[0-9]+)/$',
        user_detail,
        name='user-detail'
    ),
]
