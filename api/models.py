from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from api.utils import humanize_time
import datetime
import urllib

class ChatMessage(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', null=False, blank=False)
    to_user = models.ForeignKey(User, related_name='to_user', null=False, blank=False)
    message = models.CharField(max_length=2000, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    url = models.URLField(max_length=300, blank=False, null=False)
    
    def __unicode__(self):
        return "Message item on %s from %s to %s" % (self.date, self.from_user, self.to_user)


class FilterListItem(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    url = models.URLField(max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(default=datetime.datetime.utcnow())
    
    class Meta:
        abstract = True
    
class WhiteListItem(FilterListItem):
    
    class Meta:
        unique_together = ('user','url')

    def __unicode__(self):
        return "Whitelist item %s for %s" % (self.url, self.user.username)

class BlackListItem(FilterListItem):
    
    class Meta:
        unique_together = ('user','url')
    
    def __unicode__(self):
        return "Blacklist item %s for %s" % (self.url, self.user.username)
    
class EyeHistoryRaw(models.Model):
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
        earliest_start = timezone.now()
        earliest_eyehist = None
        total_messages = []
        
        for hist in dup_histories:
            if hist.start_time < earliest_start:
                earliest_start = hist.start_time
                earliest_eyehist = hist
            if self.favIconUrl == '' and hist.favIconUrl != '':
                self.favIconUrl = hist.favIconUrl
            
            messages = EyeHistoryMessage.objects.filter(eyehistory=hist)
            total_messages.extend(list(messages))
                
        if earliest_eyehist == None:
            earliest_eyehist = dup_histories[0]

        self.start_event = earliest_eyehist.start_event
        self.start_time = earliest_eyehist.start_time

        elapsed_time = self.end_time - self.start_time
        self.total_time = int(round((elapsed_time.microseconds / 1.0E3) + (elapsed_time.seconds * 1000) + (elapsed_time.days * 8.64E7)))
        self.humanize_time = humanize_time(elapsed_time)
        
        dup_histories.delete()
        
        return total_messages
    
    def save(self, save_raw=True, *args, **kwargs):
        
        #save raw eyehistory
        if save_raw:
            raw, created = EyeHistoryRaw.objects.get_or_create(user=self.user, 
                                        url=self.url, 
                                        title=self.title, 
                                        start_event=self.start_event, 
                                        end_event=self.end_event,
                                        start_time=self.start_time,
                                        end_time=self.end_time,
                                        src=self.src,
                                        domain=self.domain,
                                        favIconUrl=self.favIconUrl,
                                        total_time=self.total_time,
                                        humanize_time=self.humanize_time)
        
        dup_histories = EyeHistory.objects.filter(user=self.user, url=self.url, title=self.title, end_time__gt=self.start_time-datetime.timedelta(minutes=5))
        
        messages = []
        if dup_histories.count() > 0:
            messages = self._merge_histories(dup_histories)
        
        if self.favIconUrl.strip() == '':
            self.favIconUrl = "http://www.google.com/s2/favicons?domain_url=" + urllib.quote(self.url)
        super(EyeHistory, self).save(*args, **kwargs)
        
        ih = EyeHistory.objects.get(id=self.id)
        
        for message in messages:
            message.eyehistory = ih
            message.save()
            
        
        
class EyeHistoryMessage(models.Model):
    message = models.CharField(max_length=300, default='')
    post_time = models.DateTimeField(auto_now_add=True)
    eyehistory = models.ForeignKey(EyeHistory, blank=True, null=True, on_delete=models.SET_NULL)

    
    class Meta:
        ordering = ['-post_time']

    def __unicode__(self):
        return "Message %s for %s" % (self.message, self.eyehistory)
