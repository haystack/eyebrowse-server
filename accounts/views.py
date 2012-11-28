from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from annoying.decorators import render_to, ajax_request

from accounts.models import *
from accounts.renderers import *

from api.models import *

from common.view_helpers import _template_values, JSONResponse, validateEmail
from common.pagination import paginator
from common.helpers import put_profile_pic


@render_to('accounts/profile.html')
def profile(request, username=None):
    """
    Own profile page
    """
    user = request.user
    follows = False
    if not username: #viewing own profile
        username = user.username
    
    else:
        follows = user.profile.follows.filter(user__username=username).exists() 


    profile_user = get_object_or_404(User, username=username)

    page = request.GET.get('page', 1)
    
    history_items = EyeHistory.objects.filter(user=profile_user).order_by('-end_time')
    history_items = paginator(page, history_items)
    return _template_values(request, page_title="Profile", navbar='nav_profile', profile_user=profile_user, history_items=history_items, follows=str(follows))

@login_required
@render_to('accounts/edit_profile.html')
def edit_profile(request):
    """
    Edit profile page
    """

    user = request.user

    if request.POST and request.is_ajax():
        success = False
        errors = {}
        data = None
        type = request.POST.get('form_type', None)

        if type == 'pic':
            pic_url = request.POST.get('pic_url')
            pic_url = put_profile_pic(pic_url, user.profile) #download and upload to our S3
            if pic_url: #no errors/less than 1mb #patlsotw
                user.profile.pic_url = pic_url
                user.profile.save()
                success = "Profile picture changed!"
            else:
                errors['pic'] = ['Oops -- something went wrong.']
        elif type == 'account-info':
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            anon_email = request.POST.get('anon_checkbox', False) == 'True'
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user.profile.anon_email = anon_email
            user.profile.save()

            success = "User info updated!"

        resp = {
            'success' : success,
            'errors': errors,
            'type' : type,
            'data' : data,
        }

        return JSONResponse(resp)

    #not post request
    whitelist = WhiteListItem.objects.filter(user=user)
    blacklist = BlackListItem.objects.filter(user=user)
    following = user.profile.follows.all()
    followers = user.profile.followed_by.all()
    rendered_following = connection_table_renderer(following, 'following', following)
    rendered_followers = connection_table_renderer(followers, 'followers', following)


    return _template_values(request, page_title="Edit Profile", navbar='nav_account', whitelist=whitelist, blacklist=blacklist, rendered_following=rendered_following, rendered_followers=rendered_followers)

@login_required
@ajax_request
@csrf_exempt
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
