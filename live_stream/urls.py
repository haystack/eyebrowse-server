from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('live_stream.views',
                       url(r'^ping/$', 'ping'),
                       url(r'^$', 'live_stream'),
                       )
