import setup_django
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notifications" in settings.INSTALLED_APPS:
    from notifications.models import NoticeType
    NoticeType.objects.get_or_create(label="new_follower", display=_("New Follower"), description=_("You have a new follower"), default=2)
    NoticeType.objects.get_or_create(label="bump_follower", display=_("Bump into a Follower"), description=_("You bumped into a follower on the same page"), default=0)
    NoticeType.objects.get_or_create(label="note_by_follower", display=_("Note by Follower"), description=_("One of your followers posted a Note on a page you've visited"), default=0)
    NoticeType.objects.get_or_create(label="chat_by_follower", display=_("Chat Message by Follower"), description=_("One of your followers posted to the Chat Board on a page you've visited"), default=0)
    NoticeType.objects.get_or_create(label="mentioned_in_chat", display=_("Mentioned in Chat"), description=_("Someone mentioned you in a chat message"), default=2)
    NoticeType.objects.get_or_create(label="mentioned_in_note", display=_("Mentioned in Note"), description=_("Someone mentioned you in a Note"), default=2)
else:
    print "Skipping creation of NoticeTypes as notification app not found"