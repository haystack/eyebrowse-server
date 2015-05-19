from django.contrib import admin

from api.models import BlackListItem
from api.models import ChatMessage
from api.models import EyeHistory
from api.models import EyeHistoryMessage
from api.models import MuteList
from api.models import WhiteListItem

admin.site.register(BlackListItem)
admin.site.register(ChatMessage)
admin.site.register(EyeHistory)
admin.site.register(EyeHistoryMessage)
admin.site.register(MuteList)
admin.site.register(WhiteListItem)
