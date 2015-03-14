from django.contrib import admin
from django.contrib.sessions.models import Session

from accounts.models import UserProfile

admin.site.register(Session)
admin.site.register(UserProfile)
