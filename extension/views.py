from django.views.decorators.clickjacking import xframe_options_exempt

from annoying.decorators import render_to, ajax_request
from django.contrib.auth.models import User
from django.db.models import Q
from common.view_helpers import JSONResponse
from api.models import ChatMessage, EyeHistory, EyeHistoryMessage
from common.templatetags.gravatar import gravatar_for_user

from eyebrowse.settings import BASE_URL
from django.utils import timezone
import datetime
from django.db.models.aggregates import Sum
from common.templatetags.filters import url_domain
from api.utils import humanize_time
from django.contrib.auth.views import redirect_to_login
from django.views.generic.simple import redirect_to
from django.db.models import Q

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
   
@xframe_options_exempt
@render_to("extension/info_prompt.html") 
def get_info(request):
    url = request.GET.get("url")
    
    domain = url_domain(url)
    my_user = request.user
    
    timestamp =  timezone.now() - datetime.timedelta(days=30)
    
    used_users = []
    
    active = []

    eyehists = EyeHistory.objects.filter((Q(url=url) | Q(domain=domain)) & Q(start_time__gt=timestamp) & ~Q(user_id=request.user.id)).order_by('-end_time').select_related()

    for eyehist in eyehists:
        if len(active) > 6:
            break
        user = eyehist.user
        if user not in used_users:
            old_level = 4
            if eyehist.end_time > (timezone.now() - datetime.timedelta(minutes=5)):
                old_level = 0
            elif eyehist.end_time > (timezone.now() - datetime.timedelta(hours=1)):
                old_level = 1
            elif eyehist.end_time > (timezone.now() - datetime.timedelta(hours=24)):
                old_level = 2
            elif eyehist.end_time > (timezone.now() - datetime.timedelta(days=7)):
                old_level = 3
            
            active.append({'username': user.username,
                        'pic_url': gravatar_for_user(user),
                        'url': '%s/users/%s' % (BASE_URL,user.username),
                        'old_level': old_level,
                        'time_ago': humanize_time(timezone.now()-eyehist.end_time)
                        })
            used_users.append(user)
    
    message = EyeHistoryMessage.objects.filter(eyehistory__url=url).select_related()
    about_message = None
    user_url = None
    username = None
    
    if message:
        about_message = humanize_time(timezone.now() - message[0].post_time) + ' ago'
        message = message[0].message

    if not about_message:
        chat_message = ChatMessage.objects.filter(url=url).select_related()
        if chat_message:
            about_message = humanize_time(timezone.now() - chat_message[0].date) + ' ago'
            message = '"%s"' % (chat_message[0].message)
            user_url = '%s/users/%s' % (BASE_URL,chat_message[0].author.username)
            username = chat_message[0].author.username
    
    if not about_message:
        about_message = ''
        message = ''
    
    return {
        'url' : url,
        'active_users': active,
        'message': message,
        'about_message': about_message,
        'user_url': user_url,
        'username': username,
    }
    
@ajax_request 
def profilepic(request):
    return redirect_to(request, gravatar_for_user(request.user));
    
@ajax_request
def active(request):
    url = request.GET.get("url", '')
    
    domain = url_domain(url)
    
    my_user = request.user

    timestamp =  timezone.now() - datetime.timedelta(minutes=30)

    active_users = User.objects.filter(eyehistory__url=url, eyehistory__start_time__gt=timestamp).select_related().distinct()

    active_dusers = User.objects.filter(eyehistory__domain=domain, eyehistory__start_time__gt=timestamp).select_related().distinct()

    res = []
    
    for user in active_users:
        if user != my_user:
            res.append({'username': user.username,
                        'pic_url': gravatar_for_user(user),
                        'resourceURI': '/api/v1/user/%s/' % user.username,
                        })
            
    dres = []
    
    for user in active_dusers:
        if user != my_user and user not in active_users:
            dres.append({'username': user.username,
                        'pic_url': gravatar_for_user(user),
                        'resourceURI': '/api/v1/user/%s/' % user.username,
                        })
    
    return {'result': {
                       'page': res,
                       'domain': dres
                       }
            }


def get_stats(visits):
    count = visits.count()
    if count == 1:
        count_text = '1 visit'
    else:
        count_text = '%s visits' % (count)
    if count == 0:
        time = '0 seconds'
    else:
        time = humanize_time(datetime.timedelta(milliseconds=visits.aggregate(Sum('total_time'))['total_time__sum']))
        
    return count_text, time

    
@ajax_request
def stats(request):
    url = request.GET.get("url", '')
    my_user = request.user

    
    my_visits = EyeHistory.objects.filter(user=my_user, url=url)
    my_count, my_time = get_stats(my_visits)
    
    total_visits = EyeHistory.objects.filter(url=url)
    total_count, total_time = get_stats(total_visits)
    
    domain = url_domain(url)
    my_dvisits = EyeHistory.objects.filter(user=my_user, domain=domain)
    my_dcount, my_dtime = get_stats(my_dvisits)
    
    total_dvisits = EyeHistory.objects.filter(domain=domain)
    total_dcount, total_dtime = get_stats(total_dvisits)
    

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

