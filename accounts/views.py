from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from common.models import *
from data_logging.models import *
from common.view_helpers import _template_values, JSONResponse, validateEmail, validate_url
from common.helpers import put_profile_pic

@login_required
def profile(request, username=None):
    """
    Own profile page
    """

    if not username:
        username = request.user.username

    profile_user = get_object_or_404(User, username=username)

    template_values = _template_values(request, page_title="Profile", navbar='nav_profile', profile_user=profile_user)

    return render_to_response('accounts/profile.html', template_values, context_instance=RequestContext(request))

@login_required
def edit_profile(request):
    """
    Edit profile page
    """

    user = request.user
    profile = user.profile

    if request.POST and request.is_ajax():
        success = False
        errors = {}
        type = request.POST.get('form_type', None)
        
        if type == "whitelist":
            url = request.POST.get('whitelist')
            errors['whitelist'] = []

            if not validate_url(url):
                if url.strip() == "":
                    errors['whitelist'].append("Enter a url!")
                else:
                    errors['whitelist'].append(url + ' is not a valid url.')

            #make sure email doesn't exists
            elif WhiteListItem.objects.filter(url=url, user_profile=profile).exists():
                    errors['whitelist'].append(url + ' you already registered this whitelist item')

            if not len(errors['whitelist']):
                whitelist_item = WhiteListItem(url=url, user_profile=profile)
                whitelist_item.save()
                success = "Added %s"%url
        
        elif type == "email":
            emails = request.POST.getlist('email')
            errors['email'] = []

            for email in emails:
                #makes sure email is valid
                if not validateEmail(email):
                    if email.strip() == "":
                        errors['email'].append("Empty email entered.")
                    else:
                        errors['email'].append(email + ' is not a valid email.')

                #make sure email doesn't exists
                elif Email.objects.filter(email=email, email__confirmed=True).exists():
                    errors['email'].append(email + ' is already registered with an account.')

            if errors['email'] == []:
                for email in emails:
                    profile.add_email(email)
                success = "Confirmation emails sent out!"

        elif type == 'pic':
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
            'errors': errors
        }

        return JSONResponse(return_obj)

    #not post request

    email_form = [{'value':user.email}]
    for email in Email.objects.filter(user_profile=profile, confirmed=True).values_list('email', flat=True):
        field = {
            'value': email
        }
        email_form.append(field)
    
    history_data = WhiteListItem.objects.filter(user_profile=profile)

    template_values = _template_values(request, page_title="Edit Profile", navbar='nav_account', email=email_form, history_data=history_data)

    return render_to_response('accounts/edit_profile.html', template_values, context_instance=RequestContext(request))