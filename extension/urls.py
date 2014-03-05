from django.conf.urls import patterns, url

urlpatterns = patterns('extension.views',
    url(r'^trackPrompt$', 'prompt'),
    url(r'^loginPrompt$', 'login'),
    url(r'^getActiveUsers$', 'active'),
)