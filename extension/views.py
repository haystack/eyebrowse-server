from django.views.decorators.clickjacking import xframe_options_exempt

from annoying.decorators import render_to, ajax_request
from django.contrib.auth.models import User
from django.db.models import Q
from common.view_helpers import JSONResponse
from api.models import ChatMessage

from django.utils import timezone
import datetime

@xframe_options_exempt
@render_to("extension/track_prompt.html")
def prompt(request):
    site = request.GET.get("site", '')
    return {
        'site' : site
    }

@xframe_options_exempt
@render_to("extension/login_prompt.html")
def login(request):
    src = request.GET.get("src", "chrome")
    return {
        'src' : src
    }
    
@ajax_request
def active(request):
    url = request.GET.get("url", '')
    my_user = request.user

    timestamp =  timezone.now() - datetime.timedelta(minutes=5)

    active_users = User.objects.filter(eyehistory__url=url, eyehistory__start_time__gt=timestamp).select_related().distinct()

    res = []
    
    for user in active_users:
        if user != my_user:
            message_num = ChatMessage.objects.filter(from_user=user, to_user=my_user, read=False, url=url).count()
            res.append({'username': user.username,
                        'pic_url': user.userprofile.pic_url,
                        'resourceURI': '/api/v1/user/%s/' % user.username,
                        'unread_messages': message_num,
                        })
    
    return {'result': res}

