from django.conf.urls import patterns, url

urlpatterns = patterns('accounts.views',

    url(r'^profile/$', 'profile_data'),
    url(r'^profile/stats$', 'profile_stats'),
)

