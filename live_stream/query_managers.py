from django.db.models import Q
from django.db.models import Sum

from api.models import *

from live_stream.renderers import *

from accounts.models import *

from common.pagination import paginator

from datetime import datetime, timedelta

from common.templatetags.filters import url_domain

import operator

def live_stream_query_manager(get_dict, req_user, return_type="html"):

    valid_params = ['timestamp', 'query', 'following', 'firehose', 'search', 'direction','filter', 'ping', 'req_user', 'username', 'limit']

    valid_types = {
        'ping' : {
            'timestamp' : get_dict.get('timestamp', datetime.now()),
            'type' : 'ping',
        },
    }
    
    search_params = {}
    for k, v in get_dict.items():
        if k in valid_params:
            search_params[k] = v
    
    type = get_dict.get('type', None)
    if type in valid_types:
        search_params = dict(search_params, **valid_types[type])

    history = history_search(req_user, **search_params)
    
    page = get_dict.get('page', 1)

    history = paginator(page, history)


    if req_user.is_authenticated():
        following = set(req_user.profile.follows.all())
    else:
        following = set([])

    return history_renderer(req_user, history, return_type,  get_dict.get('template'), get_param=search_params.get('filter'), following=following)



def history_search(req_user, timestamp=None, query=None, filter='following', type=None, direction='hl', orderBy="start_time", limit=None, username=None):

    history = EyeHistory.objects.all()
    try:
        
        if query:
            history = history.filter(Q(title__contains=query) | Q(url__contains=query))
        
        if filter == 'following' and req_user.is_authenticated():
            history = req_user.profile.get_following_history(history=history)
        
        if username:
            history = history.filter(user__username=username)
        
        orderBy = "-" + orderBy
        if direction == 'lh':
            orderBy = orderBy[1:]
        history = history.order_by(orderBy)
        

        #ping data with latest time and see if time is present
        ## must be last
        if type == 'ping' and timestamp:
            history = history.filter(start_time__gt=timestamp)

        if limit:
            history = history[:limit]
            
    except Exception as e:
        print "EXCEPTION", e
        history = []

    return history.select_related()

def profile_stat_gen(profile_user, url=None):
    """
        Helper to calculate total time spent for a given user.
        If a url is present, the queryset is filtered to reduce the set to only this url
    """
 
    history_items = history_search(profile_user, filter="", username=profile_user.username)

    if url:
        history_items = history_items.filter(url=url)

    history_items = history_items.annotate(total=Sum('total_time'))

    tot_time = 0
    for item in history_items:
        tot_time += item.total_time


    return tot_time, history_items.count()

def fav_site_calc(profile_user):
    """
        Helper to compute what the most commonly used
        site is for a given set of history items.
        Returns a url (domain) that is computed to be the favorite and the associated favicon
    """

    item_meta = {}

    history_items = history_search(profile_user, filter="",username=profile_user.username)

    if not history_items:
        return {
                "fav_icon" : "",
                "count" : 0,
                "total_time" : "",
                "domain" : ""
            }
    
    for item in history_items:

        domain = url_domain(item.url)

        if domain in item_meta:
            data = item_meta[domain] 
            data["count"] +=1
            data["total_time"] += item.total_time
            item_meta[domain] = data
        else:
            item_meta[domain] = {
                "fav_icon" : item.favIconUrl,
                "count" : 1,
                "total_time" : item.total_time,
                "domain" : domain
            }
    
    max_count = 0
    max_dict = {}
    for k, v in item_meta.items():
        if v["count"] > max_count:
            max_count = v["count"]
            max_dict = v

    return max_dict



def online_user_count():
    """
        Computes all of the users from the history items from the last 5 minutes
    """
    timestamp =  datetime.now() - timedelta(minutes=5)

    history = EyeHistory.objects.filter(start_time__gt=timestamp).select_related()

    users = set()
    for h in history:
        if not h.user in users:
            users.add(h.user)
    return len(users)
