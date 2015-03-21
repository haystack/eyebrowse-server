import setup_django
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notifications" in settings.INSTALLED_APPS:
    from notifications.models import NoticeType
    NoticeType.create("new_follower", _("New Follower"), _("You have a new follower"))
    
    
else:
    print "Skipping creation of NoticeTypes as notification app not found"