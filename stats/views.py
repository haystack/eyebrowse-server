import json

from datetime import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic.simple import redirect_to

from ipware.ip import get_ip
from annoying.decorators import render_to, ajax_request

from accounts.models import UserProfile

from api.models import EyeHistory

from common.constants import EMPTY_SEARCH_MSG
from common.view_helpers import _get_query
from common.view_helpers import _template_values

from eyebrowse.log import logger

from live_stream.query_managers import live_stream_query_manager
from live_stream.query_managers import profile_stat_gen
from live_stream.query_managers import online_user

from stats.models import FavData, ClickItem

@login_required
@render_to('stats/follow_data.html')
def following_data(request, username=None):

    if request.user.username == username:
        username = None

    username, follows, profile_user, empty_search_msg, nav_bar = _profile_info(
        request.user, username, following=True)

    # stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)

    following_users = profile_user.profile.follows.all()

    following_count = following_users.count()
    follower_count = UserProfile.objects.filter(
        follows=profile_user.profile).count()

    follow = follow_list(following_users, profile_user, empty_search_msg)

    template_dict = {
        'username': profile_user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        "profile_user": profile_user,
        "empty_search_msg": empty_search_msg,
        "follows": str(follows),
        "is_online": is_online,
        'follow_list': follow,
        "num_history": num_history,
        "tot_time": tot_time,
        "item_count": item_count,
        "fav_data": fav_data,
    }

    return _template_values(request,
                            page_title="following list",
                            navbar=nav_bar,
                            sub_navbar="subnav_data",
                            **template_dict)


@login_required
@render_to('stats/follow_data.html')
def followers_data(request, username=None):

    if request.user.username == username:
        username = None

    username, follows, profile_user, empty_search_msg, nav_bar = _profile_info(
        request.user, username, followers=True)

    # stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)

    followers = UserProfile.objects.filter(follows=profile_user.profile)

    following_count = profile_user.profile.follows.count()
    follower_count = followers.count()

    follow = follow_list(followers, profile_user, empty_search_msg)

    template_dict = {
        'username': profile_user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        "profile_user": profile_user,
        "empty_search_msg": empty_search_msg,
        "follows": str(follows),
        "is_online": is_online,
        'follow_list': follow,
        "num_history": num_history,
        "tot_time": tot_time,
        "item_count": item_count,
        "fav_data": fav_data,
    }

    return _template_values(request,
                            page_title="followers list",
                            navbar=nav_bar,
                            sub_navbar="subnav_data",
                            **template_dict)


@render_to('stats/profile_viz.html')
def profile_viz(request, username=None):

    if request.GET.get("date") is None or request.GET.get("date") == "null":
        return redirect_to(request,
                           "/users/%s/visualizations?date=last week&query=%s" %
                           (username, request.GET.get("query", "")))

    if request.user.is_authenticated():
        user = get_object_or_404(User, username=request.user.username)
        userprof = UserProfile.objects.get(user=user)
        confirmed = userprof.confirmed
        if not confirmed:
            return redirect('/consent')
    else:
        user = None
        userprof = None

    username, follows, profile_user, empty_search_msg, nav_bar = _profile_info(
        user, username)

    get_dict, query, date, sort, filter = _get_query(request)
    logger.info(get_dict)
    logger.info(date)

    get_dict["orderBy"] = "end_time"
    get_dict["direction"] = "hl"
    get_dict["filter"] = ""
    get_dict["page"] = request.GET.get("page", 1)
    get_dict["username"] = profile_user.username
    get_dict["sort"] = "time"

    hist, history_stream = live_stream_query_manager(get_dict, profile_user)

    # stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)

    following_count = profile_user.profile.follows.count()
    follower_count = UserProfile.objects.filter(
        follows=profile_user.profile).count()

    today = datetime.now() - timedelta(hours=24)
    day_count = hist.filter(start_time__gt=today
                            ).values('url', 'title'
                                     ).annotate(num_urls=Sum('total_time')
                                                ).order_by('-num_urls')[:3]
    day_domains = hist.filter(
        start_time__gt=today
    ).values('domain'
             ).annotate(num_domains=Sum('total_time')
                        ).order_by('-num_domains')[:5]

    day_chart = {}
    for domain in day_domains:
        day_chart[domain['domain']] = domain['num_domains']

    last_week = today - timedelta(days=7)
    week_count = hist.filter(start_time__gt=last_week).values(
        'url', 'title'
    ).annotate(num_urls=Sum('total_time')
               ).order_by('-num_urls')[:3]
    week_domains = hist.filter(
        start_time__gt=last_week
    ).values('domain'
             ).annotate(num_domains=Sum('total_time')
                        ).order_by('-num_domains')[:5]

    week_chart = {}
    for domain in week_domains:
        week_chart[domain['domain']] = domain['num_domains']

    template_dict = {
        'visualization': True,
        'username': profile_user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        "profile_user": profile_user,
        "history_stream": history_stream,
        "empty_search_msg": empty_search_msg,
        "follows": str(follows),
        "is_online": is_online,
        "num_history": num_history,
        "tot_time": tot_time,
        "item_count": item_count,
        "fav_data": fav_data,
        "query": query,
        "date": date,
        'day_articles': day_count,
        'week_articles': week_count,
        'day_chart': json.dumps(day_chart),
        'week_chart': json.dumps(week_chart),

    }

    return _template_values(
        request,
        page_title="profile history",
        navbar=nav_bar,
        sub_navbar="subnav_data",
        **template_dict)


@render_to('stats/profile_data.html')
def profile_data(request, username=None):

    if request.user.is_authenticated():
        user = get_object_or_404(User, username=request.user.username)
        userprof = UserProfile.objects.get(user=user)
        confirmed = userprof.confirmed
        if not confirmed:
            return redirect('/consent')
    else:
        user = None
        userprof = None

    """
        Own profile page
    """
    username, follows, profile_user, empty_search_msg, nav_bar = _profile_info(
        user, username)

    get_dict, query, date, sort, filter = _get_query(request)

    get_dict["orderBy"] = "end_time"
    get_dict["direction"] = "hl"
    get_dict["filter"] = ""
    get_dict["page"] = request.GET.get("page", 1)
    get_dict["username"] = profile_user.username
    get_dict["sort"] = "time"

    hist, history_stream = live_stream_query_manager(get_dict, request.user, empty_search_msg=empty_search_msg)

    # stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)

    following_count = profile_user.profile.follows.count()
    follower_count = UserProfile.objects.filter(
        follows=profile_user.profile).count()

    today = datetime.now() - timedelta(hours=24)

    day_count = hist.filter(
        start_time__gt=today
    ).values('url', 'title').annotate(
        num_urls=Sum('total_time')
    ).order_by('-num_urls')[:3]

    day_domains = hist.filter(
        start_time__gt=today
    ).values('domain'
             ).annotate(num_domains=Sum('total_time')
                        ).order_by('-num_domains')[:5]

    day_chart = {}
    for domain in day_domains:
        day_chart[domain['domain']] = domain['num_domains']

    last_week = today - timedelta(days=7)

    week_count = hist.filter(
        start_time__gt=last_week
    ).values('url', 'title'
             ).annotate(num_urls=Sum('total_time')
                        ).order_by('-num_urls')[:3]

    week_domains = hist.filter(
        start_time__gt=last_week
    ).values('domain'
             ).annotate(num_domains=Sum('total_time')
                        ).order_by('-num_domains')[:5]

    week_chart = {}
    for domain in week_domains:
        week_chart[domain['domain']] = domain['num_domains']

    template_dict = {
        'username': profile_user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        "profile_user": profile_user,
        "history_stream": history_stream,
        "empty_search_msg": empty_search_msg,
        "follows": str(follows),
        "is_online": is_online,
        "num_history": num_history,
        "tot_time": tot_time,
        "item_count": item_count,
        "fav_data": fav_data,
        "query": query,
        "date": date,
        'day_articles': day_count,
        'week_articles': week_count,
        'day_chart': json.dumps(day_chart),
        'week_chart': json.dumps(week_chart),
    }

    return _template_values(request,
                            page_title="profile history",
                            navbar=nav_bar,
                            sub_navbar="subnav_data",
                            **template_dict)


def _profile_info(user=None, username=None, following=False, followers=False):
    """
        Helper to give basic profile info for
        rendering the profile page or its child pages
    """

    follows = False
    nav_bar = ""
    
    if user:
        if (not username) or (user.username == username):  # viewing own profile
            nav_bar = "nav_profile"
            username = user.username
            if following:
                msg_type = 'self_following'
            elif followers:
                msg_type = 'self_followers'
            else:
                msg_type = 'self_profile_stream'
        else:
            follows = user.profile.follows.filter(
                user__username=username).exists()
            if following:
                msg_type = 'following'
            elif followers:
                msg_type = 'followers'
            else:
                msg_type = 'profile_stream'
    else:
        if following:
            msg_type = 'following'
        elif followers:
            msg_type = 'followers'
        else:
            msg_type = 'profile_stream'

    empty_search_msg = EMPTY_SEARCH_MSG[msg_type]

    profile_user = get_object_or_404(User, username=username)

    return username, follows, profile_user, empty_search_msg, nav_bar

@ajax_request
def clicked_item(request):
    try:
        logger.info(request)
        if request.user.is_authenticated():
            user = get_object_or_404(User, username=request.user.username)
        else:
            user = None
        ip = get_ip(request)
        url_click = request.POST.get('url_click')
        url_refer = request.POST.get('url_refer')
        recommendation = request.POST.get('recommendation', None)

        c = ClickItem(user=user, ip_address=ip, url_clicked=url_click, url_referrer=url_refer)

        if recommendation:
            c.recommendation = True

        c.save()
        
    except Exception, e:
        logger.info(e)
        
    return {'res': True}

def follow_list(follows, req_user, empty_search_msg):

    template_values = {
        'following': follows,
        'user': req_user,
        'empty_search_msg': empty_search_msg,
    }

    return render_to_string('stats/follow_list.html', template_values)
