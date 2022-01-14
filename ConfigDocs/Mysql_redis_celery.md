### 导入数据库

安装mysql以后创建数据库并导入数据文件

```
mysql> create database dailyfresh; 
mysql> use dailyfresh; 
mysql> set names utf8;
mysql> source "path"/dailyfresh.sql # path 为数据文件所在路径
```

### 启动redis和celery
安装了redis和celery之后，进入redis安装目录启动redis
```
redis-server redis.windows.conf
```
注意这里celery 依赖redis作为message broker  
进入Django项目文件夹，激活虚拟环境，启动celery
```
celery -A celery_tasks.tasks worker --loglevel=info -P eventlet
```
