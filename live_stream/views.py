from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect

from annoying.decorators import render_to, ajax_request

from common.view_helpers import _template_values, _get_query

from live_stream.query_managers import *

@login_required
@render_to('live_stream/live_stream.html')
def live_stream(request):

    user = request.user

    tot_time, num_history, num_online = _get_stats(user)

    get_dict, query, date = _get_query(request)

    print get_dict

    history_stream = live_stream_query_manager(get_dict, user)

    template_dict = {
        'query' : query,
        'date' : date,
        'history_stream' : history_stream,
        'tot_time' : tot_time,
        'num_history' : num_history,
        'num_online' : num_online,
    }

    return _template_values(request, page_title="live stream", navbar="nav_home", sub_navbar=_get_subnav(request), **template_dict)

@login_required
@ajax_request
def ping(request):

    get_dict, query, date = _get_query(request)

    history = live_stream_query_manager(get_dict, request.user, return_type="list")

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
