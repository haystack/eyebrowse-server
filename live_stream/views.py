from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from accounts.models import UserProfile
from api.models import EyeHistory

from annoying.decorators import ajax_request
from annoying.decorators import render_to

from common.view_helpers import _get_query
from common.view_helpers import _template_values

from live_stream.query_managers import live_stream_query_manager
from live_stream.query_managers import online_user
from live_stream.query_managers import online_user_count
from live_stream.query_managers import profile_stat_gen
from notifications.models import Notification
from django.views.generic.simple import redirect_to



@render_to('live_stream/wordcloud_viz.html')
def word_cloud_viz(request):

    if request.GET.get("date") is None or request.GET.get("date") == "null" or request.GET.get("date") == "":
        return redirect_to(request,
                           "/visualizations/word_cloud/?filter=%s&date=last week&query=%s" %
                           (request.GET.get("filter"),
                            request.GET.get("query", "")))

    template_dict = viz_page(request)
    template_dict['viz'] = 'word'

    return _template_values(
        request,
        page_title="live stream",
        navbar="nav_home",
        sub_navbar=_get_subnav(request),
        **template_dict)

@render_to('live_stream/hod_viz.html')
def hod_viz(request):
    if request.GET.get("date") is None or request.GET.get("date") == "null" or request.GET.get("date") == "":
        return redirect_to(request,
                           "/visualizations/hour_of_day/?filter=%s&date=last week&query=%s" %
                           (request.GET.get("filter"),
                            request.GET.get("query", "")))

    template_dict = viz_page(request)
    template_dict['viz'] = 'hod'

    return _template_values(
        request,
        page_title="live stream",
        navbar="nav_home",
        sub_navbar=_get_subnav(request),
        **template_dict)

@render_to('live_stream/dow_viz.html')
def dow_viz(request):
    if request.GET.get("date") is None or request.GET.get("date") == "null" or request.GET.get("date") == "":
        return redirect_to(request,
                           "/visualizations/day_of_week/?filter=%s&date=last week&query=%s" %
                           (request.GET.get("filter"),
                            request.GET.get("query", "")))

    template_dict = viz_page(request)
    template_dict['viz'] = 'dow'

    return _template_values(
        request,
        page_title="live stream",
        navbar="nav_home",
        sub_navbar=_get_subnav(request),
        **template_dict)

def viz_page(request):
    user = request.user


    get_dict, query, date, sort, filter = _get_query(request)

    get_dict["orderBy"] = "end_time"
    get_dict["direction"] = "hl"
    get_dict["filter"] = ""
    get_dict["page"] = request.GET.get("page", 1)
    get_dict["sort"] = "time"

    hist, history_stream = live_stream_query_manager(get_dict, user)


    if user.is_authenticated():
        following_count = user.profile.follows.count()
        follower_count = UserProfile.objects.filter(follows=user.profile).count()
        tot_time, num_history = _get_stats(user, filter=filter)
    else:
        following_count = 0
        follower_count = 0
        tot_time = None
        num_history = None

    # stats
    template_dict = {
        'visualization': True,
        'username': user.username,
        "history_stream": history_stream,
        "start_time": get_dict["start_time"],
        "end_time": get_dict["end_time"],
        "query": query,
        "date": date,
        'following_count': following_count,
        'follower_count': follower_count,
        'sort': '',
        'filter': filter,
        'tot_time': tot_time,
        'num_history': num_history,
        'num_online': online_user_count(),
    }

    return template_dict

@render_to('live_stream/live_stream.html')
def live_stream(request):

    user = request.user

    get_dict, query, date, sort, filter = _get_query(request)
    hist, history_stream = live_stream_query_manager(get_dict, user)

    if user.is_authenticated():
        following_count = user.profile.follows.count()
        follower_count = UserProfile.objects.filter(follows=user.profile).count()
        tot_time, num_history = _get_stats(user, filter=filter)
    else:
        following_count = 0
        follower_count = 0
        tot_time = None
        num_history = None

    template_dict = {
        'username': user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        'query': query,
        'date': date,
        'sort': sort,
        'filter': filter,
        'history_stream': history_stream,
        'tot_time': tot_time,
        'num_history': num_history,
        'num_online': online_user_count(),
    }

    return _template_values(request,
                            page_title="live stream",
                            navbar="nav_home",
                            sub_navbar=_get_subnav(request),
                            **template_dict)


@ajax_request
def ping(request):
    get_dict, query, date, sort, filter = _get_query(request)

    get_dict["sort"] = "time"

    _, history = live_stream_query_manager(
        get_dict, request.user, return_type="list")

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
        'history': history,
        'num_history': objs.count(),
        'num_online': online_user_count(),
        'is_online': online_user(user),
    }


def _get_stats(user, filter=filter):
    """
        Helper to _get_stats
    """
    if filter == "following":
        tot_time, num_history = profile_stat_gen(
            user, filter=filter, username="")
    else:
        tot_time, num_history = profile_stat_gen(user, username="")

    return tot_time, num_history


def _get_subnav(request):
    """
        Give proper active state to obj
    """
    return "subnav_" + request.GET.get('filter', "following")
