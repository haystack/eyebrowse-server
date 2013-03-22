import os
import sys

path = '/eyebrowse-server'
if path not in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'eyebrowse.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()