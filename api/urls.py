from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^whitelist/add/$', 'whitelist_add'),
    url(r'^typeahead/$', 'typeahead'),
    
    url(r'^graphs/word_cloud$', 'word_cloud'),
    url(r'^graphs/timeline_hour', 'timeline_hour'),
    url(r'^graphs/timeline_day', 'timeline_day'),
)