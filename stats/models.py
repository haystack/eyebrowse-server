from django.contrib.auth.models import User
from django.db import models


    
class ClickItem(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    ip_address = models.CharField(max_length=39, editable=False)
    url_referrer = models.URLField(max_length=1000, default='')
    url_clicked = models.URLField(max_length=1000, default='')
    time = models.DateTimeField(auto_now_add=True)
    recommendation = models.BooleanField(default=False)
    

class FavData(models.Model):

    """
        Model to hold favorite data that
        is updated according to django cron tasks
    """
    user = models.ForeignKey(User)

    domain = models.URLField(max_length=2000, default='')
    favicon_url = models.TextField(default='')
    favIconUrl = models.URLField(max_length=2000, default='')

    visit_count = models.IntegerField(blank=True, null=True)
    total_time = models.IntegerField(blank=True, null=True)  # store in ms

    def __unicode__(self):
        return "FavData item %s for %s visited %s" % (self.domain, self.user.username, self.visit_count)
