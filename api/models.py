from django.db import models
from django.utils import simplejson as json
from django.contrib.auth.models import User
from accounts.models import *

from datetime import datetime

class FilterListItem(models.Model):
    user = models.ForeignKey(User)

    url = models.URLField(max_length=2000, default='')
    date_created = models.DateTimeField(auto_now=True, default=datetime.now())
    
class WhiteListItem(FilterListItem):
    type = models.CharField(max_length=40, default='whitelist')

    def __unicode__(self):
          return "Whitelist item %s for %s" % (self.url, self.user.username)

class BlackListItem(FilterListItem):
    type = models.CharField(max_length=40, default='blacklist')
    
    def __unicode__(self):
          return "Blacklist item %s for %s" % (self.url, self.user.username)

class EyeHistory(models.Model):
    user = models.ForeignKey(User)

    tabId = models.CharField(max_length=40, default='')
    url = models.URLField(max_length=2000, default='')
    favIconUrl = models.URLField(max_length=2000, default='')
    title = models.CharField(max_length=40, default='')

    start_event = models.CharField(max_length=40, default='')
    start_time = models.DateTimeField()

    end_event = models.CharField(max_length=40, default='')
    end_time = models.DateTimeField()

    total_time = models.IntegerField() # store in ms
    humanize_time = models.CharField(max_length=200, default='') # store as human readable according to moment.js library: http://momentjs.com/docs/#/displaying/humanize-duration/


    def __unicode__(self):
          return "EyeHistory item %s for %s on %s" % (self.url, self.user.username, self.start_time)