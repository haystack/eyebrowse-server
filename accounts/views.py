from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to, ajax_request

from accounts.renderers import *

from api.models import *

from common.view_helpers import _template_values, JSONResponse
from common.helpers import put_profile_pic

@login_required
@render_to('accounts/whitelist.html')
def whitelist(request):
    """
        Edit whitelist entries 
    """

    whitelist = WhiteListItem.objects.filter(user=request.user)

    return _template_values(request, page_title="edit whitelist", header="whitelist", navbar='nav_account', sub_navbar="subnav_whitelist", whitelist=whitelist)

@login_required
@render_to('accounts/account.html')
def account(request):
    """
        Edit account info 
    """

    user = request.user

    if request.POST and request.is_ajax():
        success = False
        errors = {}
        data = None
        type = request.POST.get('form_type', None)
        print request.POST  
        if type == 'account-info':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            anon_email = request.POST.get('anon_checkbox', False) == 'True'
            location = request.POST.get('location', '')
            website = request.POST.get('website', '')
            bio = request.POST.get('bio', '')
            
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            profile = user.profile
            profile.anon_email = anon_email
            profile.location = location
            profile.website = website
            profile.bio = bio
            profile.save()

            success = "User info updated!"

        elif type == 'pic':
            pic_url = request.POST.get('pic_url')
            pic_url = put_profile_pic(pic_url, user.profile) #download and upload to our S3
            if pic_url: #no errors/less than 1mb #patlsotw
                user.profile.pic_url = pic_url
                user.profile.save()
                success = "Profile picture changed!"
            else:
                errors['pic'] = ['Oops -- something went wrong.']

        resp = {
            'success' : success,
            'errors': errors,
            'type' : type,
            'data' : data,
        }

        return JSONResponse(resp)

    return _template_values(request, page_title="edit whitelist", header="account info", navbar='nav_account', sub_navbar="subnav_account_info")

@login_required
@render_to('accounts/connections.html')
def connections(request):
    """
        Edit connection (following/followers)
    """

    following = request.user.profile.follows.all()
    followers = request.user.profile.followed_by.all()
    rendered_following = connection_table_renderer(following, 'following', following)
    rendered_followers = connection_table_renderer(followers, 'followers', following)

    template_dict = {
        "rendered_followers" : rendered_followers,
        "rendered_following" : rendered_following,
        "header" : connections,
    }

    return _template_values(request, page_title="edit connections", navbar='nav_account', sub_navbar="subnav_connections", **template_dict)

@login_required
@ajax_request
def connect(request):

    success = False
    errors = {}
    data = None
    req_prof = request.user.profile

    if request.POST and request.is_ajax():
        
        type = request.POST.get('type', None)
        username = request.POST.get('user', None)

        if type and username:
            user = User.objects.filter(username=username)
            if user.exists():
                user = user[0]
            else:
                user = None
            
            if not user:
                errors['user'] = "Requested user %s not found."%username

            elif user.profile == req_prof:
                errors['user'] = "Cannot follow yourself."

            else:
                if type == 'add-follow':
                    req_prof.follows.add(user.profile)
                elif type == 'rm-follow' and req_prof.follows.filter(user=user).exists():
                    req_prof.follows.remove(user)
        
            success = True
            data = {
                'type' : type,
                'user' : username,
            }

        else:
            errors['user'] = 'Username required. Provided %s as username.' % username
            errors['type'] = 'Type required. Provided %s as type.' % type

    resp = {
        'success' : success,
        'errors': errors,
        'data' : data,
    }

    return resp
