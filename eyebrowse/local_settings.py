from django.conf import settings
from os import environ as env

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
BASE_URL = settings.BASE_URL_DEV

env['AWS_BUCK'] = env['AWS_BUCK_DEV']

DATABASES['default'] = {
   'ENGINE': 'django.db.backends.mysql',
   'NAME': env['MYSQL_NAME_LOCAL'],
   'HOST': env['MYSQL_HOST_LOCAL'],
   'USER': env['MYSQL_USER_LOCAL'],
   'PASSWORD': env['MYSQL_PASSWORD_LOCAL'],
   'PORT': ''
}
