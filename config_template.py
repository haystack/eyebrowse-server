# ######### Django settings ###########
ADMIN_INFO = (
    ('', ''),
)

SECRET_KEY = ''

# ####### MYSQL #########
MYSQL_PROD = {
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
}

MYSQL_LOCAL = {
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
}

# ######### EMAIL ###############
EMAIL = {
    'EMAIL_HOST': '',
    'EMAIL_HOST_USER': '',
    'EMAIL_HOST_PASSWORD': '',
    'EMAIL_PORT': 587,
    'EMAIL_USE_TLS': True,
}


# ##### Filepicker.io ##########
FILEPICKER = {
    'API_KEY': '',
}

# ############ AWS ################
# setup instructions
# http://aws.amazon.com/articles/3998?_encoding=UTF8&jiveRedirect=1
AWS = {
    'AWS_ACCESS_KEY_ID': '',
    'AWS_SECRET_ACCESS_KEY': '',
    'BUCKET': '',
    'BUCKET_DEV': '',
}

# ########### Twitter ################

TWITTER_CONSUMER_KEY = ''
TWITTER_CONSUMER_SECRET = ''

# ########### Delicious #############

DELICIOUS_CONSUMER_KEY = ''
DELICIOUS_CONSUMER_SECRET = ''

EYEBROWSE_DELICIOUS_ACCOUNT = ''

# ########### Google #############

GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
GOOGLE_SCOPE = ""
