from django.db import models
from django.utils import simplejson as json
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from common.admin import email_templates, utils
from django.conf import settings

from datetime import datetime, timedelta

import sha, random

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    #other fields here

    activation_key = models.CharField(max_length=40, default='')
    pic_url = models.CharField(max_length=1000, default="/static/common/img/placeholder.png")
    use_tour = models.BooleanField(default=True)

    def to_json(self):
        return json.dumps({
            'username': self.user.username,
            'name' : self.user.first_name + " " + self.user.last_name,
            })

    def add_email(self, email):
        email = Email(user_profile=self, email=email)
        email.send_confirm_email();
        email.save()

    def __unicode__(self):
          return "%s's profile" % self.user

class Email(models.Model):
    user_profile = models.ForeignKey(UserProfile)

    email = models.EmailField(default='')
    confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, default=datetime.now())
    activation_key = models.CharField(max_length=40, default=sha.new(sha.new(str(random.random())).hexdigest()[:5]).hexdigest())

    def send_confirm_email(self):
        content = email_templates.alt_email['content'] % (self.user_profile.user.first_name, self.email, settings.BASE_URL + '/confirm_email/' + self.activation_key + '/')
        subject = email_templates.alt_email['subject']
        emails = [self.email]
        utils.send_mail(subject, content, emails)

        self.rm_expired_emails() #perform cleanup of unconfirmed emails

    def confirm(self):
        self.confirmed = True
        self.save()

    def rm_expired_emails(self):
        time_threshold = datetime.now() - timedelta(hours=24)
        Email.objects.filter(date_created__lt=time_threshold, confirmed=False).delete()

    def __unicode__(self):
        return "%s, confirmed: %s, owned by %s" % (self.email, self.confirmed, self.user_profile.user.username)

User.profile = property(lambda u: u.get_profile())

import signals
signals.setup()