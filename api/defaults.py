PROTOCALS = ('http://', 'https://', '')

def get_urls(domain, www=False):
    
    urls = ["%s%s.com"]
    
    if www:
        urls.append("%swww.%s.com")

    return flatten(map(lambda url: map(lambda protocol: 
        url % (protocol, domain), PROTOCALS), urls))

def flatten(l):
    return [item for sublist in l for item in sublist]

"""
If adding values to this list, must run resource_helpers.wipe_blacklists() in shell
"""
DEFAULT_BLACKLIST = set(flatten([
    get_urls('google', www=True),
    get_urls('maps.google'),
    get_urls('mail.google'),
    get_urls('plus.google'),
    get_urls('drive.google'),
    get_urls('docs.google'),
    get_urls('images.google'),
    get_urls('bing'),
    get_urls('mail.yahoo'),
    get_urls('search.yahoo'),
    get_urls('duckduckgo'),
    get_urls('hotmail'),
    get_urls('facebook', www=True),
    ('chrome-devtools',),
    ('chrome',),
    ('localhost',),
]))
