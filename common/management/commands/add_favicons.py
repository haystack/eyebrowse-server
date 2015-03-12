from django.core.management.base import NoArgsCommand

from api.models import EyeHistory

import base64
import requests

GOOGLE_FAVICON_URL = "http://www.google.com/s2/favicons?domain_url="


def get_favicon_url(favicon_url, url):
    if not favicon_url or not str(favicon_url).strip():
        favicon_url = GOOGLE_FAVICON_URL + urllib.quote(url)
    return favicon_url


def convert_img_to_base64(url):
    """
        Try to download the image and convert it to base64
    """
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        return base64.b64encode(r.raw)
    return ""


class Command(NoArgsCommand):
    help = 'Convert favicon urls to Base64 format'

    def handle(self, *args, **options):
        self.stdout.write('Beginning update...\n')
        favicon_cache = {}

        for count, obj in enumerate(EyeHistory.objects.all()):

            if not count % 100:
                self.stdout.write('Updated %s \n' % count)

            favicon_url = get_favicon_url(obj.favicon_url, obj.url)
            favicon_b64 = favicon_cache.get(favicon_url)

            if favicon_b64 is None:
                favicon_b64 = convert_img_to_base64(favicon_url)
                favicon_cache[favicon_url] = favicon_b64

            obj.favicon_url = favicon_b64
            obj.save()

        self.stdout.write('Update complete.\n')
