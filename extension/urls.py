from django.conf.urls import patterns, include, url

urlpatterns = patterns('extension.views',
    url(r'^$', 'prompt'),
)