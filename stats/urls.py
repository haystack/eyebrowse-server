from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('stats.views',
                       url(r'^click_item$', 'clicked_item'),
                       )
