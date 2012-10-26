from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
    
    url(r'^whitelist/rm$', 'whitelist_rm'),
    url(r'^whitelist/add$', 'whitelist_add'),
    url(r'^data/add$', 'data_add'),
    url(r'^data/(?P<username>.+)$', 'data_get'),
    url(r'^data/search/$', 'data_search'),

)