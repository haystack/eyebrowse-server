from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from api.utils import humanize_time
import datetime
import urllib

class MuteList(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    domain = models.URLField(max_length=300, blank=False, null=False)
    
    class Meta:
        unique_together = ('user','domain')

class Tag(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    name = models.CharField(max_length=80, blank=False, null=False)
    color = models.CharField(max_length=10, blank=False, null=False)
    domain = models.URLField(max_length=300, default='')
    
class ChatMessage(models.Model):
    author = models.ForeignKey(User, related_name='author', null=False, blank=False)
    message = models.CharField(max_length=2000, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    url = models.URLField(max_length=300, blank=False, null=False)
    
    
    def __unicode__(self):
        return "Chat message item on %s by %s" % (self.date, self.author)


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

    
    def save(self, save_raw=True, *args, **kwargs):
        if self.favIconUrl.strip() == '':
            self.favIconUrl = "http://www.google.com/s2/favicons?domain_url=" + urllib.quote(self.url)
        super(EyeHistory, self).save(*args, **kwargs)
            
        
        
class EyeHistoryMessage(models.Model):
    message = models.CharField(max_length=300, default='')
    post_time = models.DateTimeField(auto_now_add=True)
    eyehistory = models.ForeignKey(EyeHistory, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-post_time']

    def __unicode__(self):
        return "Message %s on %s" % (self.message, self.post_time)
    
    

class PopularHistoryInfo(models.Model):
    url = models.URLField(max_length=255, unique=True)
    
    img_url = models.URLField(max_length=2000, default='')
    description = models.TextField(default='')
    
    domain = models.URLField(max_length=100, default='')
    favIconUrl = models.URLField(max_length=2000, default='')
    title = models.CharField(max_length=2000, default='')
 

class PopularHistory(models.Model):
   
    user = models.ForeignKey(User, null=True)
    
    popular_history = models.ForeignKey(PopularHistoryInfo, null=False)
    eye_hists = models.ManyToManyField(EyeHistory)
    visitors = models.ManyToManyField(User, related_name='pophist_visitors')
    messages = models.ManyToManyField(EyeHistoryMessage)
    top_score = models.FloatField(default=0.0)     # unique visitors + avg_time_spent + num_comments / avg_time_ago
    unique_visitor_score = models.FloatField(default=0.0)    # unique visitors / avg_time_ago
    avg_time_spent_score = models.FloatField(default=0.0)   # avg_time_spent / avg_time_ago
    num_comment_score = models.FloatField(default=0.0)   # avg_time_spent / avg_time_ago
    
    total_time_spent = models.IntegerField(default=0)    # store in ms
    total_time_ago = models.IntegerField(default=0)    # store in rounded hours
     
    humanize_avg_time = models.CharField(max_length=200, default='')
    avg_time_ago = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "popular_history")
   
def save_raw_eyehistory(user, url, title, start_event, end_event, start_time, end_time, src, domain, favIconUrl):
    elapsed_time = end_time - start_time
    total_time = int(round((elapsed_time.microseconds / 1.0E3) + (elapsed_time.seconds * 1000) + (elapsed_time.days * 8.64E7)))
    hum_time = humanize_time(elapsed_time)
    
    if favIconUrl == None:
        favIconUrl = "http://www.google.com/s2/favicons?domain_url=" + urllib.quote(url)
    
    raw, created = EyeHistoryRaw.objects.get_or_create(user=user, 
                            url=url, 
                            title=title, 
                            start_event=start_event, 
                            end_event=end_event,
                            start_time=start_time,
                            end_time=end_time,
                            src=src,
                            domain=domain,
                            favIconUrl=favIconUrl,
                            total_time=total_time,
                            humanize_time=hum_time)
    
def merge_histories(dup_histories, end_time, end_event):
    earliest_start = timezone.now()
    earliest_eyehist = None
    dup_histories = list(dup_histories)
    
    for hist in dup_histories:
        if hist.start_time < earliest_start:
            earliest_start = hist.start_time
            earliest_eyehist = hist
            
    if earliest_eyehist == None:
        earliest_eyehist = dup_histories[0]

    earliest_eyehist.end_time = end_time
    earliest_eyehist.end_event = end_event
    
    elapsed_time = earliest_eyehist.end_time - earliest_eyehist.start_time
    earliest_eyehist.total_time = int(round((elapsed_time.microseconds / 1.0E3) + (elapsed_time.seconds * 1000) + (elapsed_time.days * 8.64E7)))
    earliest_eyehist.humanize_time = humanize_time(elapsed_time)
    
    if earliest_eyehist.favIconUrl.strip() == '':
        earliest_eyehist.favIconUrl = "http://www.google.com/s2/favicons?domain_url=" + urllib.quote(earliest_eyehist.url)
    
    earliest_eyehist.save()
    
    if len(dup_histories) > 1:
        for item in dup_histories:
            if item != earliest_eyehist:
                messages = EyeHistoryMessage.objects.filter(eyehistory=item)
                for message in messages:
                    message.eyehistory = earliest_eyehist
                    message.save()
                item.delete()
            
    return earliest_eyehist
