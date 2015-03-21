from django.conf.urls import patterns, url

from .views import NoticeSettingsView


urlpatterns = patterns(
    "",
    url(r"^settings/$", NoticeSettingsView.as_view(), name="notification_notice_settings"),
)
