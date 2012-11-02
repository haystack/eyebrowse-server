from api.models import *
from accounts.models import *
from common.models import *
from django.contrib import admin

admin.site.register(UserProfile)
admin.site.register(WhiteListItem)
admin.site.register(BlackListItem)
admin.site.register(EyeHistory)
