#!usr/bin/python
# -*- coding:utf-8 -*-

from celery import task

@task()
def do_some_async_task():
    """
    Do some async task via Celery
    """
    return None
