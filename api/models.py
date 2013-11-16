from django.db import models
from django.contrib.auth.models import User

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

    src = models.CharField(max_length=40, default='')
    url = models.URLField(max_length=2000, default='')
    domain = models.URLField(max_length=2000, default='')
    favIconUrl = models.URLField(max_length=2000, default='')
    title = models.CharField(max_length=2000, default='')

    start_event = models.CharField(max_length=40, default='')
    start_time = models.DateTimeField()

    end_event = models.CharField(max_length=40, default='')
    end_time = models.DateTimeField()

    total_time = models.IntegerField() # store in ms
    
    # store as human readable according to moment.js library: http://momentjs.com/docs/#/displaying/humanize-duration/
    humanize_time = models.CharField(max_length=200, default='') 
    
    def __unicode__(self):
        return "EyeHistory item %s for %s on %s" % (self.url, self.user.username, self.start_time)
    
    def _merge_histories(self, dup_histories):
        earliest_start = datetime.datetime.now()
        earliest_eyehist = None
        for hist in dup_histories:
            if hist.start_time < earliest_start:
                earliest_start = hist.start_time
                earliest_eyehist = hist

        self.start_event = earliest_eyehist.start_event
        self.start_time = earliest_eyehist.start_time

        elapsed_time = self.end_time - self.start_time
        self.total_time = (elapsed_time.microseconds / 1.0E6)
        self.humanize_time = humanize_time(self.total_time)
        
        dup_histories.delete()
    
    def save(self, *args, **kwargs):
        dup_histories = EyeHistory.objects.filter(user=self.user, url=self.url, title=self.title, end_time__gt=self.start_time-datetime.timedelta(minutes=5))
        if dup_histories.count() > 0:
            self._merge_histories(dup_histories)
        super(EyeHistory, self).save(*args, **kwargs)
            
            