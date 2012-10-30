from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.views',
    url(r'^whitelist/add/$', 'whitelist_add'),
    url(r'^data/search/$', 'data_search'),

)