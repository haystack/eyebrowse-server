from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from accounts.models import *
from api.models import *
from common.view_helpers import _template_values, JSONResponse, NotImplementedResponse

from common.decorators import assert_post_request
from common.view_helpers import validate_url
###whitelist functionality

@login_required
#@assert_post_request
def whitelist_add(request):
    """
    API endpoint to add a whitelist item
    """
    user = request.user
    success = False
    errors = {}
    data = None
    type = request.POST.get('form_type', None)
    
    if request.POST and request.is_ajax():
        
        if type == "whitelist":
            url = request.POST.get('whitelist')
            errors['whitelist'] = []
            data = {'url' : url}
            if not validate_url(url):
                if url.strip() == "":
                    errors['whitelist'].append("Enter a url!")
                else:
                    errors['whitelist'].append(url + ' is not a valid url.')

            elif WhiteListItem.objects.filter(url=url, user=user).exists():
                    errors['whitelist'].append('You already registered the whitelist item %s'%url)

            if not len(errors['whitelist']):
                whitelist_item = WhiteListItem(url=url, user=user)
                whitelist_item.save()
                data['id'] = whitelist_item.id
                success = "Added %s"%url

    return_obj = {
        'success' : success,
        'errors': errors,
        'type' : type,
        'data' : data,
    }

    return JSONResponse(return_obj)

@csrf_exempt
@login_required
#@assert_post_request
def whitelist_rm(request):
    """
    API endpoint to remove an item from the whitelist.
    """
    user = request.user
    url = request.POST.get('url', None)

    res = {'success' : False, 'errors' : []}
    
    if not url:
        res['errors'].append('url required')
        return JSONResponse(res)
    
    whitelist_item = WhiteListItem.objects.filter(user=user, url=url)

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