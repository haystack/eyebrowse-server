from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.shortcuts import HttpResponse

from django.conf import settings

from tastypie.api import Api

from api.resources import UserResource
from api.resources import UserProfileResource
from api.resources import WhiteListItemResource
from api.resources import BlackListItemResource
from api.resources import EyeHistoryResource
from api.resources import EyeHistoryMessageResource
from api.resources import ChatMessageResource
from api.resources import MuteListResource
from api.resources import LoginResource

from eyebrowse.views import about
from eyebrowse.views import faq
from eyebrowse.views import tutorial
from eyebrowse.views import mft, mft_results_treatment, mft_results_control
from eyebrowse.views import api_docs
from eyebrowse.views import consent_accept
from eyebrowse.views import consent
from eyebrowse.views import getting_started


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(UserProfileResource())
v1_api.register(WhiteListItemResource())
v1_api.register(BlackListItemResource())
v1_api.register(EyeHistoryResource())
v1_api.register(EyeHistoryMessageResource())
v1_api.register(ChatMessageResource())
v1_api.register(MuteListResource())
v1_api.register(LoginResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/doc/',
                           include('django.contrib.admindocs.urls')),
                       url(r'^admin/', include(admin.site.urls)),

                       url(r'', include('django.contrib.auth.urls')),
                       url(r'^static/(?P<path>.*)$',
                           'django.views.static.serve',
                           {'document_root': settings.STATIC_ROOT}),
                       url(r'^robots\.txt$', lambda r: HttpResponse(
                           "User-agent: *\nDisallow: /",
                           mimetype="text/plain")),

                       url(r'^users/(?P<username>.+?)/visualizations$',
                           'stats.views.profile_viz'),
                       url(r'^users/(?P<username>.+)$',
                           'stats.views.profile_data'),
                       url(r'^following/(?P<username>.+)$',
                           'stats.views.following_data'),
                       url(r'^followers/(?P<username>.+)$',
                           'stats.views.followers_data'),

                       url(r"^notifications/", include("notifications.urls")),
                       url(r'^notifications', 'notifications.views.notifications'),

                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^live_stream/', include('live_stream.urls')),
                       
                       url(r'^visualizations/word_cloud/$', 'live_stream.views.word_cloud_viz'),
                        url(r'^visualizations/hour_of_day/$', 'live_stream.views.hod_viz'),
                        url(r'^visualizations/day_of_week/$', 'live_stream.views.dow_viz'),
                       
                       
                       url(r'^stats/', include('stats.urls')),
                       url(r'^api/', include('api.urls')),
                       url(r'^api/', include(v1_api.urls)),

                       url(r'^about', about),
                       url(r'^tutorial', tutorial),
                       url(r'^faq', faq),
                       url(r'^mft/(?P<token>.+)$', mft),
                       url(r'^mft_results/827', mft_results_treatment),
                       url(r'^mft_results/543', mft_results_control),
                       url(r'^api_docs', api_docs),

                       url(r'^consent_accept$', consent_accept),
                       url(r'^consent$', consent),
                       url(r'^getting_started$', getting_started),

                       url(r'^ext/', include("extension.urls")),
                       url(r'^tags/', include("tags.urls"))
                       
                       )

urlpatterns += patterns('eyebrowse.views',
                        url(r'^google3a0cf4e7f8daa91b.html$', 'google_verify'),
                        url(r'^feedback$', 'feedback'),
                        url(r'^add_tag$', 'add_tag'),
                        url(r'^delete_tag$', 'delete_tag'),
                        url(r'^color_tag$', 'color_tag'),
                        url(r'^downloads$', 'downloads'),
                        url(r'^$', 'home'),
                        url(r'^tracking/', include('tracking.urls')),
                        )