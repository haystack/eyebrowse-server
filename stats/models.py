from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class FavData(models.Model):

    """
        Model to hold favorite data that is updated according to django cron tasks
    """
    user = models.ForeignKey(User)

    domain = models.URLField(max_length=2000, default='')
    favicon_url = models.TextField()

    visit_count = models.IntegerField(blank=True, null=True)
    total_time = models.IntegerField(blank=True, null=True)  # store in ms

    def __unicode__(self):
        return "FavData item %s for %s visited %s" % (self.domain, self.user.username, self.visit_count)
