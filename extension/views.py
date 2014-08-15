from django.views.decorators.clickjacking import xframe_options_exempt

from annoying.decorators import render_to, ajax_request
from django.contrib.auth.models import User
from django.db.models import Q
from common.view_helpers import JSONResponse
from api.models import ChatMessage, EyeHistory
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
    
    timestamp =  timezone.now() - datetime.timedelta(minutes=30)
    
    active_users = []
    
    active_users.extend(list(User.objects.filter(eyehistory__url=url, 
                                                 eyehistory__start_time__gt=timestamp).select_related().distinct().exclude(id=my_user.id)))

    if len(active_users) < 6:
        active_users.extend(list(User.objects.filter(eyehistory__domain=domain, 
                                                     eyehistory__start_time__gt=timestamp).select_related().distinct().exclude(id=my_user.id)))
        active_users = list(set(active_users))

    if len(active_users) >= 6:
        active_users = active_users[0:6]
    else:
        older_users = []
        allow = 6 - (len(active_users))
        timestamp2 =  timestamp - datetime.timedelta(days=30)
        older_users.extend(list(User.objects.filter(eyehistory__url=url, 
                                                    eyehistory__start_time__gt=timestamp2, 
                                                    eyehistory__start_time__lt=timestamp).select_related().distinct().exclude(id=my_user.id)))
        
        if len(older_users) < allow:
            older_users.extend(list(User.objects.filter(eyehistory__domain=domain, 
                                                        eyehistory__start_time__gt=timestamp2, 
                                                        eyehistory__start_time__lt=timestamp).select_related().distinct().exclude(id=my_user.id)))
            older_users = list(set(older_users))
            
        if len(older_users) > allow:
            older_users = older_users[0:allow]
        
    active = []
    
    for user in active_users:
        e = EyeHistory.objects.filter((Q(url=url) | Q(domain=domain)) & Q(user=user)).order_by('-end_time')[0]
        active.append({'username': user.username,
                    'pic_url': gravatar_for_user(user),
                    'url': '%s/users/%s' % (BASE_URL,user.username),
                    'time_ago': humanize_time(timezone.now()-e.end_time)
                    })
    older = []
    
    for user in older_users:
        e = EyeHistory.objects.filter((Q(url=url) | Q(domain=domain)) & Q(user=user)).order_by('-end_time')[0]
        older.append({'username': user.username,
                    'pic_url': gravatar_for_user(user),
                    'url': '%s/users/%s' % (BASE_URL,user.username),
                    'time_ago': humanize_time(timezone.now()-e.end_time)
                    })
    
    
    return {
        'url' : url,
        'active_users': active,
        'older_users': older,
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

