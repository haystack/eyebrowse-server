from tastypie.serializers import Serializer
from api.models import *

import urlparse

def split_url(url):
    parsed = urlparse.urlparse(url)
    domain = parsed.netloc
    protocol = parsed.scheme
    return domain, protocol

def in_Whitelist(url):
    return in_FilterSet(WhiteListItem, url)

def in_Blacklist(url):
    return in_FilterSet(BlackListItem, url)

def in_FilterSet(set_type, url):
    domain, protocol = split_url(url)
    return (set_type.objects.filter(url=domain).exists() or set_type.objects.filter(url=protocol).exists() or set_type.objects.filter(url=url).exists())

def get_WhiteListItem(url):
    return get_FilterSetItem(WhiteListItem, url)

def get_BlackListItem(url):
    return get_FilterSetItem(BlackListItem, url)

def get_FilterSetItem(set_type, url):
    domain, protocol = split_url(url)
    urls = [domain, protocol, url]
    for item in urls:
        item_set = set_type.objects.filter(url=item)
        if item_set.exists():
            return item_set[0]
    return None

def get_username(bundle):
    """
    Requires a bundle object from obj_create
    Returns None if no user data is present in the bundle
    """
    try:
        return bundle.data['user'].split('/')[-1]
    except:
        return None

class urlencodeSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencode']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencode': 'application/x-www-form-urlencoded',
        }
    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content): 
        pass