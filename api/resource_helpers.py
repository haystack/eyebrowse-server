from tastypie.serializers import Serializer

from api.models import BlackListItem
from api.models import WhiteListItem
from api.defaults import DEFAULT_BLACKLIST

import urlparse


def get_port(bundle):
    """
        Helper to get the port from the bundle.
        Returns the port value or the default value
        of 80 if the port is empty
    """
    port = bundle.data['port']
    if not port:
        port = 80  # default port
    return port


def split_url(url):
    parsed = urlparse.urlparse(url)
    domain = parsed.netloc
    protocol = parsed.scheme
    return domain, protocol


def in_Whitelist(url, port):
    return in_FilterSet(WhiteListItem, url, port)


def in_Blacklist(url, port):
    return in_FilterSet(BlackListItem, url, port)


def in_FilterSet(set_type, url, port):
    domain, protocol = split_url(url)
    return (set_type.objects.filter(
        url=domain).exists() or set_type.objects.filter(
            url=protocol).exists() or
        set_type.objects.filter(url=url).exists())


def get_WhiteListItem(url, port):
    return get_FilterSetItem(WhiteListItem, url, port)


def get_BlackListItem(url, port):
    return get_FilterSetItem(BlackListItem, url, port)


def get_FilterSetItem(set_type, url, port):
    domain, protocol = split_url(url)
    urls = [domain, protocol, url]
    for item in urls:
        item_set = set_type.objects.filter(url=item, port=port)
        if item_set.exists():
            return item_set[0]
    return None


def wipe_blacklists():
    for url in DEFAULT_BLACKLIST:
        bad_filters = WhiteListItem.objects.filter(url=url)
        if bad_filters.exists():
            for f in bad_filters:
                print 'deleting filter %s' % f
                f.delete()


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

    def from_urlencode(self, data, options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v) > 1 else v[0])
                  for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self, content):
        pass
