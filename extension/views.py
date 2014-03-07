from django.views.decorators.clickjacking import xframe_options_exempt

from annoying.decorators import render_to, ajax_request
from django.contrib.auth.models import User
from django.db.models import Q
from common.view_helpers import JSONResponse
from api.models import ChatMessage, EyeHistory
from common.templatetags.gravatar import gravatar_for_user

from django.utils import timezone
import datetime
from django.db.models.aggregates import Sum
from common.templatetags.filters import url_domain
from api.utils import humanize_time

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
                        'pic_url': gravatar_for_user(user),
                        'resourceURI': '/api/v1/user/%s/' % user.username,
                        'unread_messages': message_num,
                        })
    
    return {'result': res}


    
@ajax_request
def stats(request):
    url = request.GET.get("url", '')
    my_user = request.user

    my_visits = EyeHistory.objects.filter(user=my_user, url=url)
    my_count = my_visits.count()
    if my_count == 0:
        my_time = '0 seconds'
    else:
        my_time = humanize_time(datetime.timedelta(milliseconds=my_visits.aggregate(Sum('total_time'))['total_time__sum']))
    
    total_visits = EyeHistory.objects.filter(url=url)
    total_count = total_visits.count()
    if total_count == 0:
        total_time = '0 seconds'
    else:
        total_time = humanize_time(datetime.timedelta(milliseconds=total_visits.aggregate(Sum('total_time'))['total_time__sum']))
    
    
    domain = url_domain(url)
    
    my_dvisits = EyeHistory.objects.filter(user=my_user, domain=domain)
    my_dcount = my_dvisits.count()
    if my_dcount == 0:
        my_dtime = '0 seconds'
    else:
        my_dtime = humanize_time(datetime.timedelta(milliseconds=my_dvisits.aggregate(Sum('total_time'))['total_time__sum']))
    

    total_dvisits = EyeHistory.objects.filter(domain=domain)
    total_dcount = total_dvisits.count()
    if total_dcount == 0:
        total_dtime = '0 seconds'
    else:
        total_dtime = humanize_time(datetime.timedelta(milliseconds=total_dvisits.aggregate(Sum('total_time'))['total_time__sum']))
    

    res = {'my_count': my_count,
           'my_time': my_time,
           'total_count': total_count,
           'total_time': total_time,
           'my_dcount': my_dcount,
           'my_dtime': my_dtime,
           'total_dcount': total_dcount,
           'total_dtime': total_dtime,
          }
    
    return {'result': res}

