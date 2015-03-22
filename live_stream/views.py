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


@login_required
@render_to('live_stream/live_stream.html')
def live_stream(request):

    user = get_object_or_404(User, username=request.user.username)
    userprof = UserProfile.objects.get(user=user)
    confirmed = userprof.confirmed
    if not confirmed:
        return redirect('/consent')

    get_dict, query, date, sort, filter = _get_query(request)

    tot_time, num_history, num_online = _get_stats(user, filter=filter)

    hist, history_stream = live_stream_query_manager(get_dict, user)

    following_count = user.profile.follows.count()
    follower_count = UserProfile.objects.filter(follows=user.profile).count()

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
        'num_online': num_online,
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

    num_online = online_user_count()

    return tot_time, num_history, num_online


def _get_subnav(request):
    """
        Give proper active state to obj
    """
    return "subnav_" + request.GET.get('filter', "following")
