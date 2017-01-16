## Stack

- OS : Ubuntu 16.04 LTS
- Nginx : Web server
- uWSGI : Connect web server and application server
- Django REST framework : Application server *(Django >= 1.10)*
- MySQL : Relational DB
- Redis : In-memory DB
- Celery : Async task manager
- Fabric : Deployment tool

## 3rd party plugins

- django-celery : Celery integration for Django
- django-suit : Admin interface
- django-silk : Live profiling and inspection tool 
- django-restframework-jwt : JSON Web Token authentication

## Directory structure
	
<pre>
	/var/www/mysite.com/
		.gitignore
		manage.py
		fabfile.py
		conf/
			nginx/
				nginx.dev.conf
				nginx.prod.conf
			uwsgi/
				mysite.ini
				uwsgi.conf
			pip/
				requirements.txt
			sensitive-fake/
				configuration.ini
				remote_server.pem
		logs/
			celery_beat.log
			celery_beat.pid
			celery_daemon.log
			celery_daemon.pid
			nginx.access.log
			nginx.error.log
			uwsgi.log
			uwsgi.pid
		mysite/
			__init__.py
			urls.py
			wsgi.py
			apps/
				main/
					__init__.py
					admin.py
					models.py
					permissions.py
					seliarizers.py
					signals.py
					tests.py
					urls.py
					views.py
				utils/
					__init__.py
					cron.py
					redis.py
					utilities.py
			settings/
				__init__.py
				base.py
				dev.py
				prod.py
</pre>


## Installation and customization

- <a href="https://github.com/ukjin1192/web-stack-wiki-and-snippets/tree/master/ubuntu-basic-settings" target="_blank">Ubuntu basic settings</a>
- <a href="https://github.com/ukjin1192/web-stack-wiki-and-snippets/tree/master/django-basic-settings" target="_blank">Django basic settings</a>
- Clone project

~~~~
$ git clone https://github.com/ukjin1192/django-rest-framework-sample
~~~~

- Rename project and configure basic settings (Assume your `{DOMAIN NAME}` is same as `{PROJECT NAME}`)

~~~~
$ mv django-rest-framework-sample/ /var/www/{DOMAIN NAME}.com/
$ cd /var/www/{DOMAIN NAME}.com/
$ mv mysite/ {DOMAIN NAME}/
~~~~

- Let `{PROJECT PATH}` as `/var/www/{DOMAIN NAME}.com/`

~~~~
$ cd {PROJECT PATH}/conf/uwsgi/
$ mv mysite.ini {DOMAIN NAME}.ini
$ vi {DOMAIN NAME}.ini

	:%s/mysite/{DOMAIN NAME}/g

$ cd {PROJECT PATH}/conf/nginx/
$ vi nginx.dev.conf nginx.prod.conf

	:%s/mysite/{DOMAIN NAME}/g
~~~~

-	Commentify `Redirect HTTP to HTTPS` block if you will not use SSL
-	Commentify `Redirect www to non-www` block if you will not redirect `www` to `non-www`

- Fill out sensitive data

~~~~
$ cd {PROJECT PATH}/conf/
$ cp -R sensitive-data/ sensitive/
$ vi configuration.ini [Fill out variables]
$ vi remote_server.pem [Fill out public certificate of remote server]
~~~~
