#!usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MyUserManager(BaseUserManager):

    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username and password
        """
        if not username:
            raise ValueError('User must have an username')
        
        if not password:
            raise ValueError('User must have a password')
        
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """
    User profile which extends AbstractBaseUser class
    AbstractBaseUser contains basic fields like password and last_login
    """
    username = models.CharField(
        verbose_name = _('Username'),
        max_length = 20,
        unique = True,
        null = False
    )
    # Email field is required to use restframework-jwt 
    email = models.EmailField(
        verbose_name = _('Email'),
        max_length = 30,
        default = ''
    )
    is_active = models.BooleanField(
        verbose_name = _('Active'),
        default = True
    )
    is_admin = models.BooleanField(
        verbose_name = _('Admin'),
        default = False
    )
    date_joined = models.DateTimeField(
        verbose_name = _('Joined datetime'),
        auto_now_add = True,
        editable = False
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    # The field named as the 'USERNAME_FIELD' for a custom user model must not be included in 'REQUIRED_FIELDS'
    REQUIRED_FIELDS = ['password', ]

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-id']

    def __unicode__(self):
        return unicode(self.username) or u''

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    """
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
    """

# Place at the end to prevent circular import errors
import main.signals
