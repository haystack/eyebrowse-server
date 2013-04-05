from django.db.models import Q

from api.models import *

from live_stream.renderers import *

from accounts.models import *

from common.pagination import paginator

from datetime import datetime

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