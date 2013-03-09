from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect

from annoying.decorators import render_to, ajax_request

from common.view_helpers import _template_values

from live_stream.query_managers import *

@render_to('live_stream/home.html')
def home(request):
    get_dict = dict(request.GET)
    if not request.user.is_authenticated() or not len(request.user.profile.follows.all()):
        get_dict["filter"] = "firehose" #default for firehose
    
    history_stream = live_stream_query_manager(get_dict, request.user)
    
    subnav = "subnav_" + get_dict.get('filter', "following")

    return _template_values(request, page_title="Live Stream", navbar="nav_home", sub_navbar=subnav, history_stream=history_stream, ping=request.GET.get('page', 1))

@ajax_request
def ping(request):
    history = live_stream_query_manager(request.GET, request.user, return_type="list")
    return {
        'history' : history
    }

def search(request):
    return home(request)