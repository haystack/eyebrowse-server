from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import redirect
from django.conf import settings

from annoying.decorators import render_to, ajax_request

from accounts.models import *

from common.admin import email_templates, utils
from common.view_helpers import _template_values, JSONResponse

#from data_stream.query_managers import *

@render_to('common/home.html')
def home(request):
    if not request.user.is_authenticated():
        return _template_values(request, page_title="home", navbar='nav_home')
    return redirect('/accounts/profile/')
    filter = request.GET.get('filter', 'following')
    

@login_required
@csrf_exempt
@ajax_request
def feedback(request):
    """
    Endpoint to submit feedback
    """
    feedback = request.POST.get('feedback', None)
    if not feedback:
        return JSONResponse({'res':'failed'})

    feedback.replace('\n', '<br>')
    user = request.user
    subject = email_templates.feedback['subject']
    content = email_templates.feedback['content'] % (user.username, feedback)
    admin_emails = [admin[1] for admin in settings.ADMINS]
    utils.send_mail(subject, content, admin_emails, from_email=user.email)
    return {'res':'success'}