from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('registration.urls')),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('eyebrowse.views', 
    url(r'^$', 'home'),
)
