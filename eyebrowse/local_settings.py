from django.conf import settings

BASE_URL = settings.BASE_URL_DEV

DATABASES['default'] = {
   'ENGINE': 'django.db.backends.sqlite3',
   'NAME': 'eyebrowse_dev.db',
   'HOST': None,
   'USER': None,
   'PASSWORD': None,
   'PORT': None
}