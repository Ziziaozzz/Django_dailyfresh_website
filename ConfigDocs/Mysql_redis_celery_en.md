### Import the database

After installing mysql, we can create the database and then import the database file.
```
mysql> create database dailyfresh; 
mysql> use dailyfresh; 
mysql> set names utf8;
mysql> source "path"/dailyfresh.sql # path is the filepath of the database file
```

### Start redis and celery
After installing redis and celery, go to the root of the installation of redis and start it.
```
redis-server redis.windows.conf
```
Notice that celery uses redis as the message broker.  
Go to the root of the django project, activate the virtual environment and start celery.
```
celery -A celery_tasks.tasks worker --loglevel=info -P eventlet
```
