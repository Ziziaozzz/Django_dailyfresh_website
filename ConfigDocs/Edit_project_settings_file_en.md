### Things need to be edited in settings.py
#### Database part:
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

#### Email part, we need to set an email address to send out the activation email to registered user:
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

#### FDFS_STORAGE_URL = ip address of ubuntu:nginx server port
```
FDFS_STORAGE_URL = 'http://ip:port/'
```
