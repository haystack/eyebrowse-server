from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to

from api.models import EyeHistory

from stats.models import FavData

from live_stream.query_managers import *

from common.view_helpers import _template_values

from common.pagination import paginator

from common.constants import *

@login_required
@render_to('stats/profile_data.html')
def profile_data(request, username=None):
    """
        Own profile page
    """
    username, follows, profile_user, empty_search_msg = _profile_info(request.user, username)

    #history
    search_params = {
        "orderBy": "end_time", 
        "direction": "hl",
        "filter" : "",
        "page" : request.GET.get("page", 1),
        "username" : profile_user.username,
    }

    history_stream = live_stream_query_manager(search_params, profile_user)

    ## stats
    tot_time, item_count = profile_stat_gen(profile_user)

    fav_data = FavData.objects.get(user=profile_user)

    num_history = EyeHistory.objects.filter(user=profile_user).count()

    is_online = online_user(user=profile_user)
    

    return _template_values(request, page_title="profile history", navbar='nav_profile', sub_navbar="subnav_data", profile_user=profile_user, history_stream=history_stream, empty_search_msg=empty_search_msg, follows=str(follows), is_online=is_online, num_history=num_history, tot_time=tot_time, item_count=item_count, fav_data=fav_data)

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