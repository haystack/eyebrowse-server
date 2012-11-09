def getURL(domain, https=False):
    protocol = 'http'
    if https:
        protocol +='s'
    return "%s://%s.com"%(protocol, domain)

DEFAULT_WHITELIST = []
DEFAULT_BLACKLIST = [
    getURL('google', https=True),
    getURL('google'),
    'localhost',
    'chrome',
    'chrome-devtools',
]