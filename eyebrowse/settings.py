# Django settings for eyebrowse project.
import os
import sys
import django

from os import environ as env
from registration_defaults.settings import *

#custom auth
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

DEBUG = (not env['DEBUG'] == 'False') #convert from string to bool

BASE_URL = 'http://www.eyebrowse.herokuapp.com'
BASE_URL_DEV = 'http://localhost:5000'

TEMPLATE_DEBUG = DEBUG

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEFAULT_EMAIL = "eyebrowse@mit.edu"

ADMINS = (
    ('Joshua Blum', 'joshblum@mit.edu'),
    ('Jason Hu', 'mjhu@mit.edu'),
    ('eyebrowse-admins', DEFAULT_EMAIL),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': env['MYSQL_NAME'],# Or path to database file if using sqlite3.
        'USER': env['MYSQL_USER'], # Not used with sqlite3.
        'PASSWORD': env['MYSQL_PASSWORD'],# Not used with sqlite3.
        'HOST':env['MYSQL_HOST'], # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',

    'compressor.finders.CompressorFinder',
)

##### settings for django-compressor
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = (
    'compressor.filters.template.TemplateFilter',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = env['SECRET_KEY']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'common.middleware.profiler.ProfileMiddleware',
     'common.middleware.crossdomainxhr.XsSharing'
)

ROOT_URLCONF = 'eyebrowse.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'eyebrowse.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    "registration_defaults",
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',

    # third party
    'compressor',
    'gunicorn',
    'django_evolution',
    'registration',
    'tastypie',
    'pagination',

    #eyebrowse
    'accounts',
    'common',
    'api',
    'live_stream',
)

APPEND_SLASH = False

#email settings from sendgrid.com
EMAIL_HOST = env['EMAIL_HOST']
EMAIL_HOST_USER = env['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = env['PASSWORD']
EMAIL_PORT = env['EMAIL_PORT']
EMAIL_USE_TLS = env['EMAIL_USE_TLS']

ACCOUNT_ACTIVATION_DAYS = 14 # Two-week activation window;


##Tastypie settings:

API_LIMIT_PER_PAGE = 0 #no default
TASTYPIE_FULL_DEBUG = DEBUG
TASTYPIE_ALLOW_MISSING_SLASH = True

XS_SHARING_ALLOWED_ORIGINS = "http://localhost:5000"

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

TASTYPIE_ALLOW_MISSING_SLASH = True


#gravatar settings
GRAVATAR_IMG_CLASS = "img-polaroid"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Include the default Django email handler for errors
        # This is what you'd get without configuring logging at all.
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
             # But the emails are plain text by default - HTML is nicer
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(SITE_ROOT, 'logs/log.log'),
        },
        # Log to a text file that can be rotated by logrotate
        'errorfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(SITE_ROOT, 'logs/error_log.log'),
        },
    },
    'loggers': {
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['errorfile'],
            'level': 'ERROR',
            'propagate': False,
            'formatter': 'simple',
        },
        # Your own app - this assumes all your logger names start with "myapp."
        'eyebrowse.views': {
            'handlers': ['logfile'],
            'level': 'INFO', # Or maybe INFO or DEBUG
            'propagate': False,
            'formatter': 'simple',
        },
    },
}


if DEBUG:
    # allowing for local_settings overides
    # how this should ultimately be set up
    # (if this is the pattern we follow)
    # is that common or default settings go in here,
    # and each different deploy location has a differnt
    # settings override that is specified by environment 
    # variable or hard code.
    
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    try:
        local_settings_file = open('eyebrowse/local_settings.py', 'r')
        local_settings_script = local_settings_file.read()
        exec local_settings_script
    except IOError:
        print "Unable to open local settings!"