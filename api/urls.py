from django.conf.urls import patterns, url

urlpatterns = patterns('api.views',
    url(r'^whitelist/add/$', 'whitelist_add'),
    url(r'^typeahead/$', 'typeahead'),
    url(r'^my_tags/$', 'my_tags'),
    url(r'^delete_eyehistory$', 'delete_eyehistory'),
    
    url(r'^graphs/word_cloud$', 'word_cloud'),
    url(r'^graphs/timeline_hour', 'timeline_hour'),
    url(r'^graphs/timeline_day', 'timeline_day'),
    url(r'^graphs/js/word_cloud$', 'word_cloud_js'),
    url(r'^graphs/js/bar_hour', 'bar_hour_js'),
    url(r'^graphs/js/bar_day', 'bar_day_js'),
)