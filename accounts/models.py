from django.db import models
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from annoying.fields import AutoOneToOneField

from common.admin import email_templates, utils

from datetime import datetime, timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #other fields here

    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    activation_key = models.CharField(max_length=40, default='')
    pic_url = models.CharField(max_length=1000, default="/static/common/img/placeholder.png")
    use_tour = models.BooleanField(default=True)
    anon_email =models.BooleanField(default=False)

    def add_email(self, email):
        email = Email(user=self, email=email)
        email.send_confirm_email();
        email.save()

    def __unicode__(self):
          return "%s's profile" % self.user

User.profile = property(lambda u: u.get_profile())

import signals
signals.setup()