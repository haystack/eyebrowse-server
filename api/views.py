from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from common.models import *
from api.models import *
from common.view_helpers import _template_values, JSONResponse, NotImplementedResponse

from common.decorators import assert_post_request

###whitelist functionality

@login_required
#@assert_post_request
def whitelist_add(request):
    """
    API endpoint to add a whitelist item
    """
    return NotImplementedResponse()

@csrf_exempt
@login_required
#@assert_post_request
def whitelist_rm(request):
    """
    API endpoint to remove an item from the whitelist.
    """
    user_profile = request.user.profile
    url = request.POST.get('url', None)

    res = {'success' : False, 'errors' : []}
    
    if not url:
        res['errors'].append('url required')
        return JSONResponse(res)
    
    whitelist_item = WhiteListItem.objects.filter(user_profile=user_profile, url=url)

    if not whitelist_item.exists():
        res['errors'].append('entry did not exist')
        return JSONResponse(res)
    
    whitelist_item = whitelist_item[0]
    whitelist_item.delete()
    res['success'] = True
    
    return JSONResponse(res)


@login_required
#@assert_post_request
def data_add(request):
    """
    API endpoint to log user data
    """
    return NotImplementedResponse()

@login_required
#@assert_post_request
def data_rm(request):
    """
    API endpoint to remove user data
    """
    return NotImplementedResponse()

@login_required
#@assert_post_request
def data_get(request, username):
    """
    API endpoint to get all data for a given user
    """
    return NotImplementedResponse()

@login_required
#@assert_post_request
def data_search(request):
    """
    General purpose search function
    """
    return NotImplementedResponse()