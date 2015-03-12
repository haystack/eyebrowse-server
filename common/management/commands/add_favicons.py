from django.core.management.base import NoArgsCommand

from api.models import EyeHistoryRaw
from api.models import EyeHistory
from api.models import PopularHistoryInfo
from stats.models import FavData

import base64
import requests
import urllib

GOOGLE_FAVICON_URL = 'http://www.google.com/s2/favicons?domain_url='
B64_HEADER = "data:image/png;base64,"


def get_favicon_url(favicon_url, url):
    if not favicon_url or not str(favicon_url).strip():
        favicon_url = GOOGLE_FAVICON_URL + urllib.quote(url)
    return favicon_url


def convert_img_to_base64(url):
    """
        Try to download the image and convert it to base64
    """
    if url.startswith(B64_HEADER):
        return url
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            encoded = base64.b64encode(r.content).replace('\n', '')
            return "%s%s" % (B64_HEADER, encoded)
    except Exception:
        pass
    return ''


def update_favicon(obj, favicon_cache):
    if isinstance(obj, FavData):
        url = obj.domain
    else:
        url = obj.url
    favicon_url = get_favicon_url(obj.favicon_url, url)
    favicon_b64 = favicon_cache.get(favicon_url)

    if favicon_b64 is None:
        favicon_b64 = convert_img_to_base64(favicon_url)
        favicon_cache[favicon_url] = favicon_b64

    obj.favicon_url = favicon_b64
    obj.save()


class Command(NoArgsCommand):
    help = 'Convert favicon urls to Base64 format'

    def handle(self, *args, **options):
        self.stdout.write('Beginning update...\n')
        favicon_cache = {}
        models = [EyeHistoryRaw, EyeHistory, PopularHistoryInfo, FavData]
        for model in models:
            self.stdout.write('Updating model %s\n' % str(model))
            for count, obj in enumerate(model.objects.all()):
                update_favicon(obj, favicon_cache)
                if not count % 100:
                    self.stdout.write('Updated %s \n' % count)

        self.stdout.write('Update complete.\n')
