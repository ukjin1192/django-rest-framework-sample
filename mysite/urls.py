# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

admin.autodiscover()

urlpatterns = [
    # Admin
    url(
        r'^admin/', 
        include(admin.site.urls)
    ),
    # Browsable API (REST framework's login and logout views) 
    url(
        r'^api-auth/', 
        include('rest_framework.urls', namespace='rest_framework')
    ),
    # JSON Web Token authentication
    url(
        r'^api-token-auth/', 
        obtain_jwt_token,
    ),
    url(
        r'^api-token-refresh/', 
        refresh_jwt_token
    ),
    url(
        r'^api-token-verify/', 
        verify_jwt_token
    ),
    # Main application
    url(
        r'^', 
        include('main.urls')
    ),
]

if settings.RUN_SILK:

    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk')),
    ]
