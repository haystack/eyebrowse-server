from django.db import models
from django.utils import simplejson as json
from accounts.models import *

from datetime import datetime


class WhiteListItem(models.Model):
    user_profile = models.ForeignKey(UserProfile)

    url = models.CharField(max_length=2000, default='')
    date_created = models.DateTimeField(auto_now=True, default=datetime.now())

    def to_json(self):
        return json.dumps({
            'url': self.url
            })

    def __unicode__(self):
          return "Whitelist item %s for %s" % (self.url, self.user_profile.user.username)

class EyeHistory(models.Model):
    user_profile = models.ForeignKey(UserProfile)

    tabId = models.CharField(max_length=40, default='')
    url = models.CharField(max_length=2000, default='')
    faviconUrl = models.CharField(max_length=2000, default='')
    title = models.CharField(max_length=40, default='')

    start_event = models.CharField(max_length=40, default='')
    start_time = models.DateTimeField()

    end_event = models.CharField(max_length=40, default='')
    end_time = models.DateTimeField()

    total_time = models.DateTimeField()

    def to_json(self):
        return json.dumps({
            'user' : self.user_profile.user.username,
            'tabId' : self.tabId,
            'url': self.url,
            'faviconUrl' : self.faviconUrl,
            'title' : self.title,
            'start_event' : self.start_event,
            'start_time' : self.start_time,
            'end_event' : self.end_event,
            'end_event' : self.end_time,
            'total_time' : self.total_time,
            }) 

    def __unicode__(self):
          return "EyeHistory item %s for %s on %s" % (self.url, self.user_profile.user.username, self.start_time)