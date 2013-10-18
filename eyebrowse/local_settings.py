from django.conf import settings

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
BASE_URL = settings.BASE_URL_DEV

settings.AWS["BUCKET"] = settings.AWS["BUCKET_DEV"]

DATABASES['default'] = {
  'ENGINE': 'django.db.backends.mysql',
  'NAME': settings.MYSQL_LOCAL["NAME"],
  'HOST': settings.MYSQL_LOCAL["HOST"],
  'USER': settings.MYSQL_LOCAL["USER"],
  'PASSWORD': settings.MYSQL_LOCAL["PASSWORD"],
  'PORT': ''
}