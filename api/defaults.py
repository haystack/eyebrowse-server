def getURL(domain, https=False, http=False, www=False):
    assert not (https and http)
    if http:
        protocol = 'http://'
    elif https:
        protocol = 'https://'
    else:
        protocol = ''
    if www:
        return "%swww.%s.com" % (protocol, domain)
    else:
        return "%s%s.com" % (protocol, domain)

"""
If adding values to this list, must run resource_helpers.wipe_blacklist() in shell
"""
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

print DEFAULT_BLACKLIST