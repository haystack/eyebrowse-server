from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

urlpatterns = patterns('accounts.views',

                       url(r'', include('registration.backends.default.urls')),

                       url(r'^profile/sharelist$', 'whitelist'),
                       url(r'^profile/account$', 'account'),
                       url(r'^profile/mutelist', 'mutelist'),
                       url(r'^profile/edit_tags', 'edit_tags'),
                       url(r'^profile/sync_twitter', 'sync_twitter'),
                       url(r'^profile/sync_delicious', 'sync_delicious'),
                       url(r'^profile/edit$', 'account'),  # old extensions
                 #      url(r'^profile/connections$', 'connections'),
                 #      url(r'^connect$', 'connect')
                       )
