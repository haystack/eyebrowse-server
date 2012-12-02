from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import redirect

from annoying.decorators import render_to, ajax_request

from common.view_helpers import _template_values

from live_stream.query_managers import *

@render_to('common/home.html')
def home(request):
    query_managers(request.GET, request.user)
    