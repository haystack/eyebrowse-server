import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils import timezone
from django.views.generic.simple import redirect_to

from annoying.decorators import ajax_request
from annoying.decorators import render_to

from api.models import ChatMessage
from api.models import EyeHistory
from api.models import EyeHistoryMessage
from api.utils import humanize_time

from common.view_helpers import JSONResponse
from common.templatetags.gravatar import gravatar_for_user
from common.templatetags.filters import url_domain

from eyebrowse.settings import BASE_URL


@xframe_options_exempt
@render_to('extension/track_prompt.html')
def prompt(request):
    site = request.GET.get('site', '')
    return {
        'site': site
    }


@xframe_options_exempt
@render_to('extension/login_prompt.html')
def login(request):
    src = request.GET.get('src', 'chrome')
    return {
        'src': src
    }


def logged_in(request):
    if request.user.is_authenticated():
        return JSONResponse({'res': True,
                             'username': request.user.username})
    else:
        return JSONResponse({'res': False})


@login_required
def popup_info(request):
    url = request.POST.get('url', '')

    domain = url_domain(url)

    timestamp = timezone.now() - datetime.timedelta(days=7)

    used_users = []

    active = []

    followers = User.objects.filter(userprofile__followed_by=request.user)

    eyehists = EyeHistory.objects.filter((
        Q(url=url) | Q(domain=domain)) &
        Q(start_time__gt=timestamp) &
        ~Q(user_id=request.user.id)
    ).order_by('-end_time').select_related()

    for eyehist in eyehists:
        if len(active) >= 6:
            break
        user = eyehist.user
        if user not in used_users and user in followers:
            old_level = 3
            if eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(minutes=5)):
                old_level = 0
            elif eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(hours=1)):
                old_level = 1
            elif eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(hours=24)):
                old_level = 2

            active.append({'username': user.username,
                           'pic_url': gravatar_for_user(user),
                           'url': '%s/users/%s' % (BASE_URL, user.username),
                           'old_level': old_level,
                           'time_ago': humanize_time(
                               timezone.now() - eyehist.end_time)
                           })
            used_users.append(user)

    messages = EyeHistoryMessage.objects.filter(
        Q(eyehistory__url=url) &
        Q(post_time__gt=timestamp)
    ).order_by('-post_time').select_related()
    about_message = None
    user_url = None
    username = None
    message = None

    for m in messages:
        if m.eyehistory.user in followers:
            message = m.message
            about_message = humanize_time(
                timezone.now() - m.post_time) + ' ago'
            user_url = '%s/users/%s' % (BASE_URL, m.eyehistory.user.username)
            username = m.eyehistory.user.username
            break

    if not about_message:
        chat_messages = ChatMessage.objects.filter(
            url=url).order_by('-date').select_related()
        for c in chat_messages:
            if c.author in followers:
                about_message = humanize_time(timezone.now() - c.date) + ' ago'
                message = '"%s"' % (c.message)
                user_url = '%s/users/%s' % (BASE_URL, c.author.username)
                username = c.author.username
                break

    if not about_message:
        about_message = ''
        message = ''

    return JSONResponse({
        'url': url,
        'active_users': active,
        'message': message,
        'about_message': about_message,
        'user_url': user_url,
        'username': username,
    })


@xframe_options_exempt
@render_to('extension/info_prompt.html')
def get_info(request):

    if not request.user.is_authenticated():
        return {
            'logged_in': False,
            'url': None,
            'active_users': None,
            'message': None,
            'about_message': None,
            'user_url': None,
            'username': None,
        }

    url = request.GET.get('url', '')

    domain = url_domain(url)

    timestamp = timezone.now() - datetime.timedelta(days=7)

    used_users = []

    active = []

    followers = User.objects.filter(userprofile__followed_by=request.user)

    eyehists = EyeHistory.objects.filter(
        (Q(url=url) | Q(domain=domain)) &
        Q(start_time__gt=timestamp) &
        ~Q(user_id=request.user.id)
    ).order_by('-end_time').select_related()

    for eyehist in eyehists:
        if len(active) >= 6:
            break
        user = eyehist.user
        if user not in used_users and user in followers:
            old_level = 3
            if eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(minutes=5)):
                old_level = 0
            elif eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(hours=1)):
                old_level = 1
            elif eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(hours=24)):
                old_level = 2

            active.append({'username': user.username,
                           'pic_url': gravatar_for_user(user),
                           'url': '%s/users/%s' % (
                               BASE_URL, user.username),
                           'old_level': old_level,
                           'time_ago': humanize_time(
                               timezone.now() - eyehist.end_time)
                           })
            used_users.append(user)

    messages = EyeHistoryMessage.objects.filter(
        Q(eyehistory__url=url) &
        Q(post_time__gt=timestamp)).select_related()
    about_message = None
    user_url = None
    username = None
    message = None

    for m in messages:
        if m.eyehistory.user in followers:
            message = m.message
            about_message = humanize_time(
                timezone.now() - message[0].post_time) + ' ago'
            break

    if not about_message:
        chat_messages = ChatMessage.objects.filter(url=url).select_related()
        for c in chat_messages:
            if c.author in followers:
                about_message = humanize_time(timezone.now() - c.date) + ' ago'
                message = '"%s"' % (c.message)
                user_url = '%s/users/%s' % (BASE_URL, c.author.username)
                username = c.author.username

    if not about_message:
        about_message = ''
        message = ''

    return {
        'logged_in': True,
        'url': url,
        'active_users': active,
        'message': message,
        'about_message': about_message,
        'user_url': user_url,
        'username': username,
    }


@xframe_options_exempt
@render_to('extension/ticker_info_prompt.html')
def get_ticker_info(request):
    return {}


@ajax_request
def profilepic(request):
    return redirect_to(request, gravatar_for_user(request.user))


      
@login_required
@ajax_request
def get_friends(request):
    
    query = request.GET.get('query', None)
    
    user_prof = UserProfile.objects.get(user=request.user)
    friends = user_prof.follows.all()
    
    data = []
    
    for friend in friends:
        if not query or query in friend.user.username:
            data.append({'id': friend.id,
                         'name': '@%s' % (friend.user.username),
                         'avatar': gravatar_for_user(friend.user),
                         'type': 'contact'})
            if len(data) > 5:
                break
    
    return {'res': data}

@login_required
@ajax_request
def get_messages(request):
    url = request.GET.get('url', '')

    timestamp = timezone.now() - datetime.timedelta(days=7)

    messages = EyeHistoryMessage.objects.filter(
        Q(eyehistory__url=url) &
        Q(post_time__gt=timestamp)
    ).order_by('-post_time').select_related()

    message_list = []
    for message in messages:
        eye_hist = message.eyehistory
        
        m = twitter_username_re.sub(lambda m: '<a href="http://eyebrowse.csail.mit.edu/users/%s">%s</a>' % (m.group(1), m.group(0)), message.message)
        
        message_list.append({'message': m,
                             'post_time': str(message.post_time),
                             'username': eye_hist.user.username,
                             'pic_url': gravatar_for_user(eye_hist.user),
                             'user_url': '%s/users/%s' % (BASE_URL, eye_hist.user.username),
                             'hum_time': humanize_time(
                                 timezone.now() - message.post_time) + ' ago'
                             })

    return {
        'result': {
            'messages': message_list,
        }
    }


@login_required
@ajax_request
def active(request):
    url = request.GET.get('url', '')

    domain = url_domain(url)

    timestamp = timezone.now() - datetime.timedelta(days=7)

    used_users = []
    active_users = []
    active_dusers = []

    eyehists = EyeHistory.objects.filter(
        (Q(url=url) | Q(domain=domain)) &
        Q(start_time__gt=timestamp) &
        ~Q(user_id=request.user.id)
    ).order_by('-end_time').select_related()

    for eyehist in eyehists:
        if len(used_users) >= 6:
            break
        user = eyehist.user
        if user not in used_users:
            old_level = 3
            if eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(minutes=5)):
                old_level = 0
            elif eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(hours=1)):
                old_level = 1
            elif eyehist.end_time > \
                    (timezone.now() - datetime.timedelta(hours=24)):
                old_level = 2

            if url == eyehist.url:
                active_users.append({'username': user.username,
                                     'pic_url': gravatar_for_user(user),
                                     'resourceURI': '%s/users/%s' % (BASE_URL, user.username),
                                     'old_level': old_level,
                                     'time_ago': humanize_time(
                                         timezone.now() - eyehist.end_time)
                                     })
            else:
                active_dusers.append({'username': user.username,
                                      'pic_url': gravatar_for_user(user),
                                      'resourceURI': '%s/users/%s' % (BASE_URL, user.username),
                                      'old_level': old_level,
                                      'time_ago': humanize_time(
                                          timezone.now() - eyehist.end_time)
                                      })
            used_users.append(user)

    return {
        'result': {
            'page': active_users,
            'domain': active_dusers
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
        time = humanize_time(datetime.timedelta(
            milliseconds=visits.aggregate(Sum('total_time'))['total_time__sum']))

    return count_text, time


@login_required
@ajax_request
def stats(request):
    url = request.GET.get('url', '')
    my_user = get_object_or_404(User, username=request.user.username)

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

    return {
        'result': res
    }
