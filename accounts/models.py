from django.db import models
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from annoying.fields import AutoOneToOneField

from api.models import EyeHistory

from datetime import datetime, timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #other fields here

    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    activation_key = models.CharField(max_length=40, default='')
    pic_url = models.CharField(max_length=1000, default=settings.DEFAULT_IMG)
    use_tour = models.BooleanField(default=True)
    anon_email =models.BooleanField(default=False)

    def get_following_history(self, history=None):
        following = self.follows.all()
        if not history:
            history = EyeHistory.objects.all()
        
        query_set = history.filter(user__in=following)
        return query_set

    def get_full_name(self):
        fullname = self.user.get_full_name()
        if fullname:
            return fullname
        return self.user.username

    def __unicode__(self):
          return "%s's profile" % self.user


User.profile = property(lambda u: u.get_profile())

import signals
signals.setup()