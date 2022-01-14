# Django_dailyfresh_project

## Project introduction
Based on Itheima Django course projects. Dailyfresh is a B2C e-commerce website project built with the Django framework. This project is built for the purpose of learning the features of Django. The project mainly includes four important aspects: user, goods, shopping cart and order. The functions of those aspects cover some of the basic needs of an e-commerce website.

### The main tech stacks：
1. Python, Django  
2. Mysql: store the data of users, goods, and orders
3. Redis: implement shopping cart's functions, store users' browser history, and work as a message broker for Celery
4. Celery: send the activation email to a user in an asynchronous way when that user registers
5. FastDFS & Nginx: store images of the website in a distributed way; convenient to scale the storage; increase the efficiency to get images
6. Haystack & Whoosh: search framework and search engine; used for the search purposes inside the website

## Architecture and functions
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Architecture%20%26%20functions.JPG)

## Installation and configuration

We need to run FastDFS in Linux. I added an ubuntu using VirtualBox on my laptop and installed the FastDFS & Nginx there. Mysql, Redis, Celery and the main project are running in another win10 computer.

### Install python packages
```
pip install -r requirements.txt
```

### Main configurations
[Mysql, Redis and Celery](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Mysql_redis_celery_en.md)  
[FastDFS and Nginx](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/FastDFS_Nginx_en.md)  
[Edit project settings file](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Edit_project_settings_file_en.md)  
[Others](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Others_en.md)  

### Migration and running
```
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

## Project images
### Index page
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_index.JPG)
### Search
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_search.JPG)
### Shopping cart
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_cart.JPG)
### Admin
![](https://github.com/Ziziaozzz/Django_dailyfresh_website/blob/master/ConfigDocs/Daily_fresh_admin.JPG)
  
  
## Bug fixes
### Fix bugs which caused incorrect results in the total and subtotal calculations in the shopping cart page.  
