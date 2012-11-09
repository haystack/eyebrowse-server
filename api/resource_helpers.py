from api.models import *

from urlparse import urlparse

def split_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    protocol = parsed.scheme
    return domain, protocol

def inWhitelist(url):
    return inFilterSet(WhiteListItem, url)

def inBlacklist(url):
    return inFilterSet(BlackListItem, url)

def inFilterSet(set_type, url):
    domain, protocol = split_url(url)
    return (set_type.objects.filter(url=domain).exists() or set_type.objects.filter(url=protocol).exists() or set_type.objects.filter(url=url).exists())

def getWhitelistItem(url):
    return getFilterSetItem(WhiteListItem, url)

def getBlacklistItem(url):
    return getFilterSetItem(BlackListItem, url)

def getFilterSetItem(set_type, url):
    domain, protocol = split_url(url)
    urls = [domain, protocol, url]
    for item in urls:
        item_set = set_type.objects.filter(url=item)
        if item_set.exists():
            return item_set[0]
    return None
