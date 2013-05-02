from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect

from annoying.decorators import render_to, ajax_request

from common.view_helpers import _template_values
from common.npl.date_parser import DateRangeParser

from live_stream.query_managers import *

@login_required
@render_to('live_stream/home.html')
def home(request):

    user = request.user
    
    history_stream = live_stream_query_manager(request.GET, user)

    tot_time, num_history, num_online = _get_stats(user)

    subnav = _get_subnav(request)

    return _template_values(request, page_title="live stream", navbar="nav_home", sub_navbar=subnav, history_stream=history_stream, tot_time=tot_time, num_history=num_history, num_online=num_online)

@login_required
@ajax_request
def ping(request):

    history = live_stream_query_manager(request.GET, request.user, return_type="list")
    username = request.GET.get("username", "")

    if username:
        objs = EyeHistory.objects.filter(user__username=username)
    else:
        objs = EyeHistory.objects.all()


    return {
        'history' : history,
        'num_history' : objs.count(),
        'num_online' : online_user_count(),
        'is_online' : online_user(username)
    }

@login_required
@render_to('live_stream/home.html')
def search(request):
    
    user = request.user

    tot_time, num_history, num_online = _get_stats(user)

    query = request.GET.get("query", "")
    date = request.GET.get("date", "")
    start_time = None
    end_time = None
    
    if date:
        start_time, end_time = DateRangeParser().parse(date)

    get_dict = {
        "query" : query,
        "filter" : request.GET.get("filter", "following"),
        "start_time" : start_time,
        "end_time": end_time,
    }


    history_stream = live_stream_query_manager(get_dict, user)

    subnav = _get_subnav(request)

    return _template_values(request, page_title="search", navbar="nav_home", sub_navbar=subnav, query=query, date=date, history_stream=history_stream, tot_time=tot_time, num_history=num_history, num_online=num_online)

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

