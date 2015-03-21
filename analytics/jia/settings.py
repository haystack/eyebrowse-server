import os
import re
from os.path import dirname as parent
import sys

APPROOT = parent(parent(parent((os.path.realpath(__file__)))))
sys.path.append(APPROOT)

from analytics.config import ANALYTICS_EMAILS
from analytics.config import GOOGLE_CLIENT_ID
from analytics.config import GOOGLE_CLIENT_SECRET
from analytics.config import SECRET_KEY

# Basic configuration settings
DEBUG = False
HOST = '0.0.0.0'
PORT = 8152
# SECRET_KEY is imported
FORCE_SSL = False
# DANGEROUS: Allow arbitrary Python queries from the browser
ALLOW_PYCODE = False
SYSTEM_EMAIL = 'eyebrowse@csail.mit.edu'  # Emails sent from here

# DEPRECATION WARNING: Communication with backend data sources is moving into
# Metis, and will be removed in the next release of Jia
KRONOS_URL = 'http://localhost:8150'
KRONOS_NAMESPACE = 'kronos'

# Precompute settings
PRECOMPUTE = False
# The cache is written here; can be the same as KRONOS_URL
CACHE_KRONOS_URL = 'http://localhost:8150'
CACHE_KRONOS_NAMESPACE = 'default_cache'
# It is not recommended to expose the scheduler outside the LAN
SCHEDULER_HOST = '127.0.0.1'
SCHEDULER_PORT = 8157
SCHEDULER_DATABASE_URI = 'sqlite:///%s/scheduler.db' % APPROOT
# When precompute query code fails, emails will be sent to the following
SCHEDULER_FAILURE_EMAILS = [
    SYSTEM_EMAIL
]

# Metis settings
METIS_URL = 'http://localhost:8151'
DATA_SOURCE_NAME = 'kronos'
DATA_SOURCE_TYPE = 'kronos'

# This database persists all dashboards and settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/app.db' % APPROOT

ENABLE_GOOGLE_AUTH = False
# Google authentication to protect your board from random users
ALLOWED_EMAILS = map(re.compile,
    # Only user IDs matching regexes in this list will be allowed to create
    # accounts
    ANALYTICS_EMAILS,
)

# GOOGLE_CLIENT_SECRET imported
# GOOGLE_CLIENT_ID imported
# Set http://yourdomain.com/google_callback as an authorized redirect URI
# when you set up your client ID at https://console.developers.google.com/
