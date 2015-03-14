from django.contrib import admin

from api.models import BlackListItem
from api.models import EyeHistory
from api.models import WhiteListItem

admin.site.register(BlackListItem)
admin.site.register(EyeHistory)
admin.site.register(WhiteListItem)
