from django.db.models import Q
from django.db.models import Sum

from api.models import *

from live_stream.renderers import *

from accounts.models import *

from common.pagination import paginator

from datetime import timedelta

from common.templatetags.filters import url_domain
from django.utils import timezone
import operator
from eyebrowse.log import logger

def live_stream_query_manager(get_dict, req_user, return_type="html"):

    valid_params = ["timestamp", "sort", "query", "following", "firehose", "direction", "filter", "ping", "req_user", "username", "limit", "orderBy", "start_time", "end_time"]

    valid_types = {
        "ping" : {
            "timestamp" : get_dict.get("timestamp", timezone.now()),
            "type" : "ping",
        },
    }
    
    search_params = {}
    for k, v in get_dict.items():
        if k in valid_params:
            search_params[k] = v
    
    type = get_dict.get("type", None)
    if type in valid_types:
        search_params = dict(search_params, **valid_types[type])

    hist_type, hist = history_search(req_user, **search_params)
    
    page = get_dict.get("page", 1)

    history = paginator(page, hist)

    if req_user.is_authenticated():
        following = set(req_user.profile.follows.all())
    else:
        following = set([])
    
    if hist_type == "eyehistory" and hasattr(history, 'object_list'):
        self_profile = False
        if search_params.get('username') == req_user.username:
            self_profile = True
        history.object_list = group_history(history.object_list, req_user, self_profile=self_profile)
    elif hasattr(history, 'object_list'):
        set_tags(history.object_list, req_user) 
    
    return hist, history_renderer(req_user, history, hist_type, return_type,  get_dict.get("template"), get_params=search_params, following=following)



def history_search(req_user, timestamp=None, query=None, sort="top", filter="following", type=None, direction="hl", orderBy="start_time", limit=None, username=None, start_time=None, end_time=None):

    hist_type = None
    
    if not username and sort != "time":
        try:
            if filter == "following" and req_user.is_authenticated():
                history = PopularHistory.objects.filter(user=req_user)    
            else:
                history = PopularHistory.objects.filter(user=None)
            
            if query:
                history = history.filter(Q(popular_history__title__icontains=query) | Q(popular_history__url__icontains=query))
        
            if start_time and end_time:
                history = history.filter(avg_time_ago__gt=start_time, avg_time_ago__lt=end_time)
            elif start_time:
                history = history.filter(avg_time_ago__gt=start_time)
        
            if req_user.is_authenticated():
                mutelist = MuteList.objects.filter(user=req_user, url__isnull=False).values_list('url', flat=True)
                if len(mutelist) > 0:
                    query = reduce(operator.and_, (~Q(popular_history__url__contains=x) for x in mutelist))
                    history = history.filter(query)
                    
                mutelist = MuteList.objects.filter(user=req_user, word__isnull=False).values_list('word', flat=True)
                if len(mutelist) > 0:
                    query = reduce(operator.and_, (~Q(popular_history__title__contains=x) for x in mutelist))
                    history = history.filter(query)


            if sort == "visits":
                history = history.order_by('-unique_visitor_score')
            elif sort == "long":
                history = history.order_by('-avg_time_spent_score')
            elif sort == "comments":
                history = history.order_by('-num_comment_score')
            else:
                history = history.order_by('-top_score')
                
            if limit:
                history = history[:limit]
                
            hist_type = "popularhistory"
       
        except Exception as e:
            print "EXCEPTION", e
            history = EyeHistory.objects.none()  
    else:
        history = EyeHistory.objects.all()
        try:
            
            if query:
                history = history.filter(Q(title__icontains=query) | Q(url__icontains=query))
            
            if filter == "following" and req_user.is_authenticated():
                history = req_user.profile.get_following_history(history=history)
            
            if username:
                history = history.filter(user__username=username)
            else:
                if req_user.is_authenticated():
                    mutelist = MuteList.objects.filter(user=req_user, url__isnull=False).values_list('url', flat=True)
                    if len(mutelist) > 0:
                        query = reduce(operator.and_, (~Q(url__contains=x) for x in mutelist))
                        history = history.filter(query)
                        
                    mutelist = MuteList.objects.filter(user=req_user, word__isnull=False).values_list('word', flat=True)
                    if len(mutelist) > 0:
                        query = reduce(operator.and_, (~Q(title__contains=x) for x in mutelist))
                        history = history.filter(query)
            
            orderBy = "-" + orderBy
            if direction == "lh":
                orderBy = orderBy[1:]
            history = history.order_by(orderBy)
    
            if start_time and end_time:
                history = history.filter(start_time__gt=start_time, end_time__lt=end_time)
            elif start_time:
                history = history.filter(start_time__gt=start_time)
            
            #ping data with latest time and see if time is present
            ## must be last
            if type == "ping" and timestamp:
                history = history.filter(start_time__gt=timestamp)
    
            if limit:
                history = history[:limit]
            
        except Exception as e:
            print "EXCEPTION", e
            history = EyeHistory.objects.none()
    
    if not hist_type:
        hist_type = "eyehistory"

    return hist_type, history.select_related()

def profile_stat_gen(profile_user, filter=None, username=None, url=None):
    """
        Helper to calculate total time spent for a given user.
        If a url is present, the queryset is filtered to reduce the set to only this url
    """
    if username is None:
        username = profile_user.username


    history_items = EyeHistory.objects.all()
    
    if username:
        history_items = history_items.filter(user__username=username)

    if filter:
        user_prof = UserProfile.objects.get(user=profile_user)
        history_items = user_prof.get_following_history()

    if url:
        history_items = history_items.filter(url=url)

 
    total_time = history_items.aggregate(total=Sum("total_time"))

    return total_time["total"], history_items.count()


def online_user_count(filter_user=None):
    """
        Returns the number of users online
    """
    return len(_online_users())


def online_user(user):
    """
        Returns boolean if a user is online
    """
    return user in _online_users()


def _online_users():
    """
        Computes all of the users from the history items from the last 5 minutes
    """
    timestamp =  timezone.now() - timedelta(minutes=5)

    history = EyeHistory.objects.filter(start_time__gt=timestamp).select_related()

    users = set()
    for h in history:
        if not h.user in users:
            users.add(h.user)
    return users

def set_tags(history, req_user):
    history = list(history)
    for h in history:
        t = Tag.objects.filter(user=req_user, domain=h.popular_history.domain)
        if t.exists():
            h.tag = t[0]

def group_history(history, req_user, self_profile=False):
    history = list(history)
    history_groups = []
    i = 0
    while i < len(history):
        group = GroupHistory(history[i], req_user)
        if not self_profile:
            url = history[i].url
            if EyeHistory.objects.filter(user=req_user, url=url).exists():
                group.visited = True
            
        j = i + 1
        while j < len(history):
            if group.domain == history[j].domain and group.user == history[j].user:
                if not self_profile:
                    url = history[j].url
                    if EyeHistory.objects.filter(user=req_user, url=url).exists():
                        if group.visited:
                            group.add_item(history[j])
                            j += 1
                        else:
                            i = j
                            break
                    else:
                        if group.visited:
                            i = j
                            break
                        else:
                            group.add_item(history[j])
                            j += 1
                else:    
                    group.add_item(history[j])
                    j += 1
            else:
                i = j
                break
        i = j
        history_groups.append(group)
        
    if not self_profile:
        for group in history_groups:
            if len(group.history_items) == 1:
                url = group.history_items[0].url
                if EyeHistory.objects.filter(user=req_user, url=url).exists():
                    group.visited = True
    
    return history_groups


    
class GroupHistory(object):
    def __init__(self, history_item, req_user):
        self.id = history_item.id
        self.domain = history_item.domain
        self.tag = None
        self.visited = False
        
        if req_user.is_authenticated():
            tag = Tag.objects.filter(user=req_user, domain=history_item.domain)
            if tag.count() > 0:
                self.tag = tag[0]
            
        self.history_items = []
        self.add_item(history_item)
        self.favIconUrl = history_item.favIconUrl
        self.user = history_item.user
    
    def add_item(self, history_item):
        history_item.messages = history_item.eyehistorymessage_set.all()
        self.history_items.append(history_item)
    
    def get_items(self):
        if len(self.history_items) == 1:
            return []
        else:
            return self.history_items[1:]
    
    def first_item(self):
        return self.history_items[0]
    

