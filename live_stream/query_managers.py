from api.models import *

from live_stream.renderers import *

from accounts.models import *

from django.db.models import Q



def live_stream_query_manager(get_dict, user, return_type="html"):

    valid_params = ['history_id', 'query', 'following', 'firehose', 'search', 'ping', 'user']

    valid_types = {
        'ping' : {
            'history_id' : get_dict.get('history_id', None), 
        },
    }
    
    search_params = {k : v for k, v in get_dict.items() if k in valid_params}
    
    type = get_dict.get('type', None)
    if type in valid_types:
        search_params = dict(search_params, **valid_types[type])

    history = history_search(**search_params)
    following = user.profile.follows.all()

    for h_item in history:
        h_item.follows = h_item.user in following
    return history_renderer(user, history, return_type, get_dict.get('page',1))



def history_search(history_id=None, query=None, filter='firehose', type='ping', user=None):

    history = EyeHistory.objects.all()
    
    try:
        #ping data with latest id and see if new id is present
        if type == 'ping' and history_id:
            history = history.filter(id__gt=history_id)

        if query:
            history = history.filter(Q(title__contains=query) | Q(url__contains=query))

        if filter == 'following' and user:
            history = user.get_following_history(history=history)

        if limit:
            history = history[:limit]
            
    except:
        history = EyeHistory.objects.all()

    return history.select_related().order_by('-start_time')