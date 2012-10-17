from django import template

register = template.Library()
import json
from django.contrib.staticfiles.storage import staticfiles_storage

def fill(template, path):
    static_path = staticfiles_storage.url(path)
    return template % static_path

@register.simple_tag
def include_script(script_name):
    return fill("""<script type="text/javascript" src="%s.js"></script>""", script_name)

@register.simple_tag
def include_style(style_name):
    return fill("""<link type="text/css" rel="stylesheet" href="%s.css" />""", style_name)