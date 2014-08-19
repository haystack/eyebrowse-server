from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect
from django.db.models import Count

from annoying.decorators import render_to, ajax_request
import json
from common.view_helpers import _template_values, _get_query

from live_stream.query_managers import *

@login_required
@render_to('live_stream/live_stream.html')
def live_stream(request):
    
    user = get_object_or_404(User, username=request.user.username)
    userprof = UserProfile.objects.get(user=user)
    confirmed = userprof.confirmed
    if not confirmed:
        return redirect('/consent')

    tot_time, num_history, num_online = _get_stats(user)

    get_dict, query, date = _get_query(request)

    hist, history_stream = live_stream_query_manager(get_dict, user)
    
    
    following_count = user.profile.follows.count()
    follower_count = UserProfile.objects.filter(follows=user.profile).count()


    today = datetime.now() - timedelta(hours=24)
    day_count = hist.filter(start_time__gt=today).values('url', 'title').annotate(num_urls=Count('id')).order_by('-num_urls')[:3]
    day_domains = hist.filter(start_time__gt=today).values('domain').annotate(num_domains=Count('id')).order_by('-num_domains')[:5]
    
    day_chart = {}
    for domain in day_domains:
        day_chart[domain['domain']] = domain['num_domains']
    
    last_week = today - timedelta(days=7)
    week_count = hist.filter(start_time__gt=last_week).values('url', 'title').annotate(num_urls=Count('id')).order_by('-num_urls')[:3]
    week_domains = hist.filter(start_time__gt=last_week).values('domain').annotate(num_domains=Count('id')).order_by('-num_domains')[:5]
    
    week_chart = {}
    for domain in week_domains:
        week_chart[domain['domain']] = domain['num_domains']
    
    
    template_dict = {
        'username': user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        'query' : query,
        'date' : date,
        'history_stream' : history_stream,
        'tot_time' : tot_time,
        'num_history' : num_history,
        'num_online' : num_online,
        'day_articles': day_count,
        'week_articles': week_count,
        'day_chart': json.dumps(day_chart),
        'week_chart': json.dumps(week_chart),
    }

    return _template_values(request, page_title="live stream", navbar="nav_home", sub_navbar=_get_subnav(request), **template_dict)

@login_required
@ajax_request
def ping(request):

    get_dict, query, date = _get_query(request)

    _, history = live_stream_query_manager(get_dict, request.user, return_type="list")

    username = request.GET.get("username", "")

    if username:
        objs = EyeHistory.objects.filter(user__username=username)

    else:
        objs = EyeHistory.objects.all()

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        user = None

    return {
        'history' : history,
        'num_history' : objs.count(),
        'num_online' : online_user_count(),
        'is_online' : online_user(user),
    }

def _get_stats(user):
    """
        Helper to _get_stats
    """
    tot_time, num_history = profile_stat_gen(user, username="")

    num_online = online_user_count()

    return tot_time, num_history, num_online

def _get_subnav(request):
    """
        Give proper active state to obj
    """
    return "subnav_" + request.GET.get('filter', "following")
