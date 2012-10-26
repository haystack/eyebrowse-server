from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from common.models import *
from api.models import *
from common.view_helpers import _template_values, JSONResponse, NotImplementedResponse

from common.decorators import assert_post_request

###whitelist functionality

@login_required
@assert_post_request
def whitelist_add(request):
    return NotImplementedResponse()

@login_required
@assert_post_request
def whitelist_rm(request):
    return NotImplementedResponse()

@login_required
@assert_post_request
def data_add(request):
    return NotImplementedResponse()

@login_required
@assert_post_request
def data_rm(request):
    return NotImplementedResponse()

@login_required
@assert_post_request
def data_get(request, username):
    return NotImplementedResponse()

@login_required
@assert_post_request
def data_search(request):
    return NotImplementedResponse()