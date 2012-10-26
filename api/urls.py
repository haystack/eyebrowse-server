from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
    
    url(r'^whitelist/rm$', 'rm_whitelist'),
    url(r'^whitelist/rm$', 'add_whitelist'),
    url(r'^data/add$', 'add_data'),
    url(r'^data/(?P<username>.+)$', 'add_data'),
    url(r'^search/$', 'search'),

)