from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core import serializers


from accounts.models import *
from api.models import *
from common.view_helpers import _template_values, JSONResponse, validateEmail
from common.helpers import put_profile_pic

@login_required
def profile(request, username=None):
    """
    Own profile page
    """

    if not username:
        username = request.user.username

    profile_user = get_object_or_404(User, username=username)

    eye_history = EyeHistory.objects.all().order_by('-end_time')

    template_values = _template_values(request, page_title="Profile", navbar='nav_profile', profile_user=profile_user, eye_history=eye_history)

    return render_to_response('accounts/profile.html', template_values, context_instance=RequestContext(request))

@login_required
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

        return_obj = {
            'success' : success,
            'errors': errors,
            'type' : type,
            'data' : data,
        }

        return JSONResponse(return_obj)

    #not post request
    whitelist = WhiteListItem.objects.filter(user=user)
    blacklist = BlackListItem.objects.filter(user=user)
    
    template_values = _template_values(request, page_title="Edit Profile", navbar='nav_account', whitelist=whitelist, blacklist=blacklist)
    print template_values
    return render_to_response('accounts/edit_profile.html', template_values, context_instance=RequestContext(request))