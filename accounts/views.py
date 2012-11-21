from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from annoying.decorators import render_to, ajax_request

from accounts.models import *
from api.models import *
from common.view_helpers import _template_values, JSONResponse, validateEmail
from common.pagination import paginator
from common.helpers import put_profile_pic

@login_required
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
    
    eye_history = EyeHistory.objects.filter(user=profile_user).order_by('-end_time')
    eye_history = paginator(page, eye_history)
    return _template_values(request, page_title="Profile", navbar='nav_profile', profile_user=profile_user, eye_history=eye_history, follows=follows)

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

        resp = {
            'success' : success,
            'errors': errors,
            'type' : type,
            'data' : data,
        }

        return JSONResponse(return_obj)

    #not post request
    whitelist = WhiteListItem.objects.filter(user=user)
    blacklist = BlackListItem.objects.filter(user=user)
    
    return _template_values(request, page_title="Edit Profile", navbar='nav_account', whitelist=whitelist, blacklist=blacklist)