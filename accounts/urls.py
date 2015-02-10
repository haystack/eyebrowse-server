from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',

    url(r'', include('registration.backends.default.urls')),
    
    url(r'^profile/whitelist$', 'whitelist'),
    url(r'^profile/account$', 'account'),
    url(r'^profile/sync_twitter', 'sync_twitter'),
    url(r'^profile/edit$', 'account'), #old extensions 
    url(r'^profile/connections$', 'connections'),
    url(r'^connect$', 'connect')
)