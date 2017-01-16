#!/bin/bash

import os
from boto3.session import Session
from ConfigParser import ConfigParser
from fabric.api import *

ROOT_DIR = os.path.dirname(__file__)

# Get sensitive configuration
config = ConfigParser()
config.read(ROOT_DIR + '/conf/sensitive/configuration.ini')

PROJECT_NAME = config.get('django', 'project_name')

@task
def localhost():
    """
    Localhost deployment
    Usage:
        $ fab local {COMMANDS}
    """
    env.run = local
    env.cd = lcd
    env.hosts = ['localhost']
    env.warn_only = True

@task
def remote():
    """
    Remote deployment
    Usage:
        $ fab remote {COMMANDS}
    """
    AWS_ACCESS_KEY_ID = config.get('aws', 'access_key_id')
    AWS_SECRET_ACCESS_KEY = config.get('aws', 'secret_access_key')
    INSTANCE_KEY_NAME = config.get('aws', 'instance_key_name')

    env.run = run
    env.cd = cd
    env.hosts = []
    env.warn_only = True
    env.user = 'ubuntu'
    env.key_filename = ROOT_DIR + '/conf/sensitive/remote_server.pem'
    env.port = 22

    session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, 
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
            region_name='ap-northeast-2')   # SEOUL REGION

    ec2_instances = session.resource('ec2')

    for instance in ec2_instances.instances.all():
        if instance.key_name == INSTANCE_KEY_NAME: 
            env.hosts.append(instance.public_dns_name)

@task(alias='ob')
def onboot():
    """
    Start services in instance boot
    """
    env.run('sudo service nginx start')
    env.run('sudo service mysql start')
    env.run('sudo service redis-server start')
    env.run('sudo service rabbitmq-server start')

@task(alias='rn')
def restart_nginx():
    """
    Restart nginx web server
    """
    env.run('sudo service nginx restart')

@task(alias='ru')
def run_uwsgi():
    """
    Run uWSGI as daemon
    """
    env.run('sudo uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals '
            + '--master --die-on-term --daemonize=' + ROOT_DIR + '/logs/uwsgi.log --disable-logging')

@task(alias='su')
def stop_uwsgi():
    """
    Stop uWSGI
    Note: `grep` and `awk` command should be wrapped with single quote
    """
    env.run("ps -ef | grep 'uwsgi' | grep -v grep | awk '{print $2}' | xargs kill -15")

@task(alias='rs')
def run_shell():
    """
    Run enhanced Django shell 
    """
    with env.cd(ROOT_DIR):
        try:
            env.run('./manage.py shell_plus')
        except:
            env.run('./manage.py shell')

@task(alias='rt')
def run_test(app_name):
    """
    Run test
    Usage:
        $ fab localhost rt:main
    """
    with env.cd(ROOT_DIR):
        env.run('./manage.py test ' + app_name)

@task(alias='rds')
def run_development_server():
    """
    Run Django's development web server
    """
    with env.cd(ROOT_DIR):
        env.run('./manage.py runserver 0.0.0.0:8000')

@task(alias='sds')
def stop_development_server():
    """
    Stop Django's development web server
    """
    env.run('sudo fuser -k 8000/tcp')

@task(alias='rc')
def run_celery():
    """
    Run Celery and Celery beat as daemon
    """
    with env.cd(ROOT_DIR):
        env.run('./manage.py celeryd_detach --logfile=logs/celery_daemon.log --pidfile=logs/celery_daemon.pid')
        env.run('./manage.py celery beat --logfile=logs/celery_beat.log --pidfile=logs/celery_beat.pid --detach')

@task(alias='sc')
def stop_celery():
    """
    Stop Celery and Celery beat
    Note: `grep` and `awk` command should be wrapped with single quote
    """
    env.run("ps auxww | grep 'celery worker' | grep -v grep | awk '{print $2}' | xargs kill -15")
    env.run("ps auxww | grep 'celery beat' | grep -v grep | awk '{print $2}' | xargs kill -15")

@task(alias='cct')
def clear_celery_tasks():
    """
    Clear async tasks from Celery
    """
    with env.cd(ROOT_DIR):
        env.run('./manage.py celery purge')

@task(alias='csl')
def clear_silk_logs():
    """
    Clear logs from django-silk
    """
    with lcd(ROOT_DIR):
        env.run('./manage.py silk_clear_request_log')

@task(alias='d')
def deploy():
    """
    Deploy after git pull
    Note: `grep` and `awk` command should be wrapped with single quote
    """
    with env.cd(ROOT_DIR):
        env.run('git pull origin master')
        env.run("ps -ef | grep 'uwsgi' | grep -v grep | awk '{print $2}' | xargs kill -15")
        env.run('uwsgi --uid www-data --gid www-data --emperor /etc/uwsgi/vassals --master --die-on-term --daemonize=' + ROOT_DIR + '/logs/uwsgi.log --disable-logging')
