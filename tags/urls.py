from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('tags.views',
                        url(r'^value_tag$', 'value_tag'),
                        url(r'^tags/page', 'tags_by_page'),
                        url(r'^page$', 'page'),
                        url(r'^initialize_page$', 'initialize_page'),
                      )