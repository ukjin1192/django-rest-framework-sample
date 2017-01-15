#!usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from main.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_active')
    search_fields = ('username', )
    list_filter = ('last_login', )
    date_hierarchy = 'last_login'
    ordering = ('-id', )

admin.site.register(User, UserAdmin)
