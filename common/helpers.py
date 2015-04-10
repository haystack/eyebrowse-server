import hashlib
import gc
import requests

from urllib import urlretrieve

from django.conf import settings

from boto.s3.connection import S3Connection
from boto.s3.key import Key


def put_profile_pic(url, profile):
    """
    Takes a url from filepicker and uploads
    it to our aws s3 account.
    """
    try:
        r = requests.get(url)
        size = r.headers.get('content-length')
        if int(size) > 10000000:  # greater than a 1mb #patlsotw
            return False

        filename, headers = urlretrieve(url + "/resize?w=600&h=600")
        # store profile sized picture (40x40px)
        resize_filename, headers = urlretrieve(url + "/resize?w=40&h=40")
        conn = S3Connection(
            settings.AWS["AWS_ACCESS_KEY_ID"],
            settings.AWS["AWS_SECRET_ACCESS_KEY"])
        b = conn.get_bucket(settings.AWS["BUCKET"])

        _set_key(b, profile.user.username, filename)
        k = _set_key(b, profile.user.username + "resize", resize_filename)

    except Exception as e:
        print e
        return False

    return "http://s3.amazonaws.com/%s/%s" % (settings.AWS["BUCKET"], k.key)


def _set_key(b, username, filename):
    k = Key(b)

    h = hashlib.new("md5")
    h.update(username)
    k.key = h.hexdigest()
    k.set_contents_from_filename(filename)
    k.set_acl('public-read')

    return k

def queryset_iterator_chunkify(queryset, chunksize=1000):
    if not queryset.exists():
      return
    pk = 0
    last_pk = queryset.order_by('-pk')[0].pk
    queryset = queryset.order_by('pk')
    while pk < last_pk:
        batch = queryset.filter(pk__gt=pk)[:chunksize]
        pk = batch[batch.count()-1].pk
        yield batch
        gc.collect()


def queryset_iterator(queryset, chunksize=1000):
    # https://djangosnippets.org/snippets/1949/
    """
    Iterate over a Django Queryset ordered by the primary key

    This method loads a maximum of chunksize (default: 1000) rows in it's
    memory at the same time while django normally would load all rows in it's
    memory. Using the iterator() method only causes it to not preload all the
    classes.

    Note that the implementation of the iterator does not support ordered query sets.
    """
    for batch in queryset_iterator_chunkify(queryset, chunksize=chunksize):
      for row in batch:
        yield row

