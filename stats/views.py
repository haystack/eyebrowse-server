from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to

from api.models import *

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

    page = request.GET.get('page', 1)

    history_items = EyeHistory.objects.filter(user=profile_user).order_by('-end_time')

    history_items = paginator(page, history_items)
    

    return _template_values(request, page_title="profile history", navbar='nav_profile', sub_navbar="subnav_data", profile_user=profile_user, history_items=history_items, empty_search_msg=empty_search_msg, ping=page, follows=str(follows))

@login_required
@render_to('stats/profile_stats.html')
def profile_stats(request, username=None):
    """
        Stats for a profile
    """
    username, follows, profile_user, empty_search_msg = _profile_info(request.user, username)


    tot_time, item_count = profile_stat_gen(profile_user)

    print tot_time, item_count


    fav_data = fav_site_calc(profile_user)


    return _template_values(request, page_title="profile stats", navbar='nav_profile', sub_navbar="subnav_stats", profile_user=profile_user, empty_search_msg=empty_search_msg, follows=str(follows), tot_time=tot_time, item_count=item_count, fav_site=fav_data["domain"], fav_favicon=fav_data["fav_icon"], fav_time=fav_data["total_time"], fav_count=fav_data["count"])

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