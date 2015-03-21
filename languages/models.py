from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Language(models.Model):

    user = models.ForeignKey(User)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)