from django.contrib.sessions.models import Session
from accounts.models import *
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(Session)