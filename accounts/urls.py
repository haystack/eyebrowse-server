from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',

    url(r'', include('registration.urls')),
    
    url(r'^profile/$', 'profile_data'),
    url(r'^profile/stats$', 'profile_stats'),
    url(r'^profile/edit$', 'edit_profile'),
    url(r'^connect$', 'connect')
)