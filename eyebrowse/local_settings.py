from django.conf import settings
from os import environ as env

BASE_URL = settings.BASE_URL_DEV

DATABASES['default'] = {
   'ENGINE': 'django.db.backends.mysql',
   'NAME': env['MYSQL_NAME_LOCAL'],
   'HOST': env['MYSQL_HOST_LOCAL'],
   'USER': env['MYSQL_USER_LOCAL'],
   'PASSWORD': env['MYSQL_PASSWORD_LOCAL'],
   'PORT': ''
}