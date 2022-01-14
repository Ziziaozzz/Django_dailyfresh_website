### 在项目settings文件中需要设置的地方
#### 数据库部分
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh',
        'HOST': 'localhost',
        'PORT': '3306',
        'USER': '',  # database username
        'PASSWORD': '',  # database password
    }
}
```

#### 邮箱部分，可以将gmail改为qq，然后在qq邮箱里设置smtp
```
#Email for django config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = '.....@gmail.com'  # email address
EMAIL_HOST_PASSWORD = ''  # email authentication code or password depending on email servers
#EMAIL_USE_TLS = True
EMAIL_FROM = 'Dailyfresh<.....@gmail.com>'  # the same as EMAIL_HOST_USER
```

#### 将fdfs url设置为ubuntu虚拟机的ip地址:nginx server port
```
FDFS_STORAGE_URL = 'http://ip:port/'
```
