from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings

from annoying.decorators import render_to, ajax_request

from accounts.models import *

from common.admin import email_templates
from common.view_helpers import _template_values

@render_to('common/about.html')
def about(request):
    return _template_values(request, page_title="home", navbar='nav_home')

@render_to('common/faq.html')
def faq(request):
    return _template_values(request, page_title="home", navbar='nav_home')

@render_to('common/api_docs.html')
def api_docs(request):
    return _template_values(request, page_title="home", navbar='nav_home')



@render_to('common/home.html')
def home(request):
    if not request.user.is_authenticated():
        return _template_values(request, page_title="home", navbar='nav_home')
    return redirect('/live_stream/')


@render_to('common/downloads.html')
def downloads(request):
    return _template_values(request, page_title="downloads", navbar='nav_home')
    

@login_required
@ajax_request
def feedback(request):
    """
    Endpoint to submit feedback
    """
    feedback = request.POST.get('feedback', None)
    if not feedback:
        return {'res':'failed'}

    feedback.replace('\n', '<br>')
    user = request.user
    subject = email_templates.feedback['subject']
    content = email_templates.feedback['content'] % (user.username, feedback)
    admin_emails = [admin[1] for admin in settings.ADMINS]
    send_mail(subject, content, from_email=user.email, recipient_list=admin_emails)
    return {'res':'success'}

@render_to('google3a0cf4e7f8daa91b.html')
def google_verify(request):
    return {}