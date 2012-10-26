from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('django.contrib.auth.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),


    url(r'^users/(?P<username>.+)$', 'accounts.views.profile'),

    url(r'^accounts/', include('accounts.urls')),
    url(r'^api/', include('api.urls')),

)

urlpatterns += patterns('eyebrowse.views',
    url(r'^confirm_email/(?P<key>\w+)', 'confirm_email'),
    url(r'^feedback$', 'feedback'),

    url(r'^$', 'home'),

)
