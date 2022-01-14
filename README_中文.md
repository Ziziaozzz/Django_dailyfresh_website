# Django_dailyfresh_project

## 项目简介
天天生鲜(Dailyfresh)是一个使用python Django框架搭建的电商网站项目，此项目基于黑马程序员课程项目，主要用于学习Django框架。  
项目包含了四个主要模块：用户，商品，购物车和订单，其功能覆盖了电商网站的一些基本需求。  
### 项目的主要技术栈如下：
```
1. Python Django  
2. Mysql 存储用户、商品和订单信息  
3. Redis 用于实现购物车功能，保存用户浏览商品的记录和作为Celery的message broker  
4. Celery 用于异步给用户发邮件，让用户在注册时不用等待网站长时间的跳转  
5. FastDFS & Nginx 分布式存储网站图片；存储容量扩展方便；提高获取图片的效率
6. Haystack & Whoosh  全文检索框架和全文检索引擎，用于站内搜索
```
## 架构和模块功能图
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/%E9%A1%B9%E7%9B%AE%E6%9E%B6%E6%9E%84%E5%92%8C%E6%A8%A1%E5%9D%97%E5%8A%9F%E8%83%BD.JPG)
## 项目安装和配置流程

FastDFS需要在Linux下运行，我是给笔记本装了VirtualBox，然后在ubuntu下安装和配置FastDFS & Nginx，其他的Mysql, Redis, Celery 以及主项目在另一台电脑win10下运行。

### 安装 python packages
```
pip install -r requirements.txt
```

### 主要配置
[Mysql, Redis and Celery](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Mysql_redis_celery.md)  
[FastDFS and Nginx](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/FastDFS_Nginx.md)  
[Edit project settings file](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Edit_project_settings_file.md)  
[Others](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Others.md)  

### 迁移和启动
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

## 项目图片
### 首页
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_index.JPG)
### 搜索
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_search.JPG)
### 购物车
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_cart.JPG)
### 后台管理
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_admin.JPG)
