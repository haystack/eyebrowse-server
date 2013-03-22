from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

from urlparse import urlparse

import time

register = template.Library()

def fill(template, path):
    static_path = staticfiles_storage.url(path)
    return template % static_path

@register.filter
def url_domain(url):
    domain = urlparse(url).netloc
    if domain:
        return domain
    return url

@register.filter
def date_ms(dt):
    return int(1000*time.mktime(dt.timetuple()))

@register.filter
def date_fmt(dt):
    print "date", dt
    return str(dt)

@register.simple_tag
def include_script(script_name):
    return fill("""<script type="text/javascript" src="%s.js"></script>""", script_name)

@register.simple_tag
def include_style(style_name):
    return fill("""<link type="text/css" rel="stylesheet" href="%s.css" />""", style_name)