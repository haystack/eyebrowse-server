from django.conf.urls import patterns, url
from django.conf.urls import url

urlpatterns = patterns('live_stream.views',
                       url(r'^ping/$', 'ping'),
                       url(r'^$', 'live_stream'),
                       )
