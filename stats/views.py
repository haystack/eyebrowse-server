from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to

from api.models import EyeHistory

from stats.models import FavData

from live_stream.query_managers import *

from common.view_helpers import _template_values, _get_query

from common.pagination import paginator

from common.constants import *

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

    history_stream = live_stream_query_manager(get_dict, profile_user)

    ## stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)
    

    template_dict = {
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
    }

    return _template_values(request, page_title="profile history", navbar='nav_profile', sub_navbar="subnav_data", **template_dict)

def _profile_info(user, username=None):
    """
        Helper to give basic profile info for rendering the profile page or its child pages
    """

    follows = False
    if not username: #viewing own profile
        username = user.username
        msg_type = 'self_profile_stream'
    
    else:
        follows = user.profile.follows.filter(user__username=username).exists()
        msg_type = 'profile_stream'
        
    empty_search_msg = EMPTY_SEARCH_MSG[msg_type]

    profile_user = get_object_or_404(User, username=username)

    return username, follows, profile_user, empty_search_msg