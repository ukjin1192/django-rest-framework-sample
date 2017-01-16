#!usr/bin/python
# -*- coding:utf-8 -*-

from celery import task

@task()
def do_some_async_task(var_1, var_2, *args, **kwargs):
    """
    Do some async task via Celery
    Usage:
        do_some_async_task.apply_async(
            args=[
                'variable 1',
                'variable 2',
                'arguments 1', 'arguments 2', 'arguments 3'
            ],
            kwargs={
                'kwargs_1': 'foo', 
                'kwargs_2': 'bar'
            }
        )
    """
    return None
