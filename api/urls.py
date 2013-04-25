from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^whitelist/add/$', 'whitelist_add'),
    url(r'^typeahead/$', 'typeahead'),
)