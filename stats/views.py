from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count

from annoying.decorators import render_to

from api.models import EyeHistory

from stats.models import FavData

from live_stream.query_managers import *

from common.view_helpers import _template_values, _get_query

from common.pagination import paginator

from common.constants import *

@login_required
@render_to('stats/notifications.html')
def notifications(request):
  
    empty_search_msg = EMPTY_SEARCH_MSG['notifications']
    user = get_object_or_404(User, username=request.user.username)
    
    ## stats
    tot_time, item_count = profile_stat_gen(user)

    fav_data = FavData.objects.get(user=user)

    num_history = EyeHistory.objects.filter(user=user).count()

    is_online = online_user(user=user)
    
    following_users = user.profile.follows.all()
    following_count = following_users.count()
    follower_count = UserProfile.objects.filter(follows=user.profile).count()
    
    notifications = notification_renderer(user, empty_search_msg)
    
    template_dict = {
        "username": user.username,
        "following_count": following_count,
        "follower_count": follower_count,
        "is_online" : is_online,
        "num_history" : num_history,
        "notifications": notifications,
        "tot_time" : tot_time,
        "item_count" : item_count,
        "fav_data" : fav_data,
    }

    return _template_values(request, page_title="notifications", navbar='notify', sub_navbar="subnav_data", **template_dict)


def notification_renderer(user, empty_search_msg):
    
    timestamp = timezone.now() - timedelta(days=7)
    
    urls = EyeHistory.objects.filter(user=user, start_time__gt=timestamp).order_by('end_time').values('url', 'end_time','start_time')
    
    url_list = {}
    for url in urls:
        url_list[url['url']] = (url['start_time'], url['end_time'])
    
    notification_list = []
    
    for url in url_list:
        visits = EyeHistory.objects.filter(Q(url=url) &
                                           ~Q(user_id=user.id) & 
                                           (Q(start_time__lte=url_list[url][1]) & 
                                            Q(end_time__gte=url_list[url][0])))
        for visit in visits:
            tmp = {}
            tmp['type'] = 'bump domain'
            tmp['url'] = url
            tmp['author'] = visit.user
            tmp['title'] = visit.title
            tmp['date'] = url_list[url][1]
            tmp['visit_time'] = humanize_time(timezone.now() - url_list[url][1])
            
            notification_list.append(tmp)
    

    messages = EyeHistoryMessage.objects.filter(Q(eyehistory__url__in=url_list.keys()) & Q(post_time__gt=timestamp) & ~Q(eyehistory__user_id=user.id)).select_related()
    chat_messages = ChatMessage.objects.filter(Q(url__in=url_list.keys()) & Q(date__gt=timestamp) & ~Q(author_id=user.id)).select_related()
    
    
    
    for m in messages:
        notification_list.append({'type': 'bulletin',
                                  'message': m.message,
                                  'date': m.post_time,
                                  'date_hum': humanize_time(timezone.now() - m.post_time),
                                  'url': m.eyehistory.url,
                                  'author': m.eyehistory.user,
                                  'title': m.eyehistory.title,
                                  'visit_time': humanize_time(timezone.now() - url_list[m.eyehistory.url][1])
                                  })
    for c in chat_messages:
        notification_list.append({'type': 'chat',
                                  'message': c.message,
                                  'date': c.date,
                                  'date_hum': humanize_time(timezone.now() - c.date),
                                  'url': c.url,
                                  'author': c.author,
                                  'title': '',
                                  'visit_time': humanize_time(timezone.now() - url_list[c.url][1])
                                  })

    notification_list = sorted(notification_list, key=lambda x: x['date'], reverse=True)
    
    template_dict = {'notifications': notification_list,
                     'empty_search_msg': empty_search_msg,}
    
    return render_to_string('stats/notification_list.html', template_dict)
    

@login_required
@render_to('stats/follow_data.html')
def following_data(request, username=None):
    
    if request.user.username == username:
        username = None
    
    username, follows, profile_user, empty_search_msg = _profile_info(request.user, username, following=True)

    ## stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)
    
    following_users = profile_user.profile.follows.all()
    
    following_count = following_users.count()
    follower_count = UserProfile.objects.filter(follows=profile_user.profile).count()
    
    follow = follow_list(following_users, profile_user, empty_search_msg)
    

    template_dict = {
        'username': profile_user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        "profile_user" : profile_user,
        "empty_search_msg" : empty_search_msg,
        "follows" : str(follows), 
        "is_online" : is_online,
        'follow_list': follow,
        "num_history" : num_history,
        "tot_time" : tot_time,
        "item_count" : item_count,
        "fav_data" : fav_data,
    }

    return _template_values(request, page_title="following list", navbar='nav_profile', sub_navbar="subnav_data", **template_dict)

    

@login_required
@render_to('stats/follow_data.html')
def followers_data(request, username=None):
    
    if request.user.username == username:
        username = None
    
    username, follows, profile_user, empty_search_msg = _profile_info(request.user, username, followers=True)

    ## stats
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
        "profile_user" : profile_user,
        "empty_search_msg" : empty_search_msg,
        "follows" : str(follows), 
        "is_online" : is_online,
        'follow_list': follow,
        "num_history" : num_history,
        "tot_time" : tot_time,
        "item_count" : item_count,
        "fav_data" : fav_data,
    }

    return _template_values(request, page_title="following list", navbar='nav_profile', sub_navbar="subnav_data", **template_dict)

    


@login_required
@render_to('stats/profile_data.html')
def profile_data(request, username=None):
    """
        Own profile page
    """
    username, follows, profile_user, empty_search_msg = _profile_info(request.user, username)

    get_dict, query, date = _get_query(request)

    get_dict["orderBy"] = "end_time"
    get_dict["direction"] = "hl"
    get_dict["filter"] = ""
    get_dict["page"] = request.GET.get("page", 1)
    get_dict["username"] = profile_user.username

    hist, history_stream = live_stream_query_manager(get_dict, profile_user)

    ## stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)
    
    following_count = profile_user.profile.follows.count()
    follower_count = UserProfile.objects.filter(follows=profile_user.profile).count()
    

    
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
        'username': profile_user.username,
        'following_count': following_count,
        'follower_count': follower_count,
        "profile_user" : profile_user,
        "history_stream" : history_stream,
        "empty_search_msg" : empty_search_msg,
        "follows" : str(follows), 
        "is_online" : is_online,
        "num_history" : num_history,
        "tot_time" : tot_time,
        "item_count" : item_count,
        "fav_data" : fav_data,
        "query" : query,
        "date" : date,
        'day_articles': day_count,
        'week_articles': week_count,
        'day_chart': json.dumps(day_chart),
        'week_chart': json.dumps(week_chart),
    }

    return _template_values(request, page_title="profile history", navbar='nav_profile', sub_navbar="subnav_data", **template_dict)

def _profile_info(user, username=None, following=False, followers=False):
    """
        Helper to give basic profile info for rendering the profile page or its child pages
    """

    follows = False
    if not username: #viewing own profile
        username = user.username
        if following:
            msg_type = 'self_following'
        elif followers:
            msg_type = 'self_followers'
        else:
            msg_type = 'self_profile_stream'
        
    else:
        follows = user.profile.follows.filter(user__username=username).exists()
        if following:
            msg_type = 'following'
        elif followers:
            msg_type = 'followers'
        else:
            msg_type = 'profile_stream'
        
    empty_search_msg = EMPTY_SEARCH_MSG[msg_type]

    profile_user = get_object_or_404(User, username=username)

    return username, follows, profile_user, empty_search_msg


def follow_list(follows, req_user, empty_search_msg):

    template_values =  {
        'following' : follows,
        'user' : req_user,
        'empty_search_msg': empty_search_msg,
    }


    return render_to_string('stats/follow_list.html',template_values)
