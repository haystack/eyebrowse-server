from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.template.loader import render_to_string

from annoying.decorators import render_to, ajax_request

from accounts.models import *
from api.models import *
from common.view_helpers import _template_values, JSONResponse, NotImplementedResponse

from common.view_helpers import validate_url

@login_required
@ajax_request
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

    return {
        'success' : success,
        'errors': errors,
        'type' : type,
        'data' : data,
    }

@ajax_request
def typeahead(request):
    query = request.GET.get('query', None)
    success =  False
    errors = "no query"
    users = None
    
    if query:
        users = User.objects.filter(
            Q(username__startswith=query) | Q(email__startswith=query, userprofile__anon_email=False)
        )
        if users.exists():
            users = [render_to_string('api/typeahead_row.html', {'user' : user}) for user in users]
            errors = None
            success = True
        else:
            errors = 'no match. query: %s' % query
            users = None
    res =  {
        'success' : success,
        'errors' : errors,
        'users' : users
    }

    return res
                
