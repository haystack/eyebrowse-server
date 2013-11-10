from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.db.models import Q

from annoying.decorators import ajax_request
from api.defaults import DEFAULT_BLACKLIST

from accounts.models import *
from api.models import *
from common.view_helpers import _template_values, JSONResponse, NotImplementedResponse
from common.templatetags.gravatar import gravatar_img_for_user
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
            
            if url in DEFAULT_BLACKLIST:
                errors['whitelist'].append("Cannot whitelist this url.")
            elif not validate_url(url):
                if url.strip() == "":
                    errors['whitelist'].append("Enter a url!")
                else:
                    errors['whitelist'].append(url + " is not a valid url.")

            elif WhiteListItem.objects.filter(url=url, user=user).exists():
                    errors['whitelist'].append("You already registered the whitelist item %s" % url)

            if not len(errors['whitelist']):
                whitelist_item = WhiteListItem(url=url, user=user)
                whitelist_item.save()
                data['id'] = whitelist_item.id
                success = "Added %s" % url

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
        users = {}
        terms = query.split()
        for term in terms:
            filtered_users = User.objects.filter(
                Q(username__istartswith=term) | Q(email__istartswith=term, userprofile__anon_email=False) | 
                Q(first_name__istartswith=term) | Q(last_name__istartswith=term)
            )
            if filtered_users.exists():
                for user in filtered_users:
                    users[user.id] = {
                        'username': user.username, 
                       'fullname': user.get_full_name(), 
                       'email': user.email, 
                       'gravatar': gravatar_img_for_user(user,24)
                    } 

        if not len(users):
            errors = 'no match. query: %s' % query
            users = None
        else:
            errors = None
            success = True
            users = users.values()
    
    res =  {
        'success' : success,
        'errors' : errors,
        'users' : users
    }

    return res
