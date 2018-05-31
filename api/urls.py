from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('api.views',
                       url(r'^rating/get$', 'rating_get'),
                       url(r'^rating/update$', 'rating_update'),
                       url(r'^whitelist/add$', 'whitelist_add'),
                       url(r'^whitelist/get$', 'whitelist_get'),
                       url(r'^mutelist/add/$', 'mutelist_add'),
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
