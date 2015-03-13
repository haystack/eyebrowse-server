from django.conf.urls import patterns, url

urlpatterns = patterns('live_stream.views',
    url(r'^ping/$', 'ping'),
    url(r'^$', 'live_stream'),
)