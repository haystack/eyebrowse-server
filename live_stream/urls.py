from django.conf.urls import patterns, include, url

urlpatterns = patterns('live_stream.views',
    
    url(r'^home/$', 'home'),
    url(r'^ping/$', 'ping'),
    url(r'^search/$', 'search')
)