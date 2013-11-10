def getURL(domain, https=False, http=False, www=False):
    protocol = 'http'
    if https:
        protocol +='s'
    return "%s://%s.com"%(protocol, domain)


DEFAULT_BLACKLIST = [
    getURL('google', https=True),
    getURL('google'),
    getURL('maps.google'),
    'localhost',
    'chrome',
    'chrome-devtools',
    getURL('mail.google', https=True),
    getURL('mail.google'),
    getURL('facebook', www=True),
    getURL('facebook', www=True, https=True),
    getURL('hotmail'),
    getURL('mail.yahoo'),
    getURL('search.yahoo'),
    getURL('bing'),
    getURL('duckduckgo'),
    
]