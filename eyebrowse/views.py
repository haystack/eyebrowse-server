from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import redirect

from django.conf import settings
from common.admin import email_templates, utils

from accounts.models import *
from common.view_helpers import _template_values, JSONResponse

def home(request):
    template_values = {}
    return render_to_response('common/base.html', template_values, context_instance=RequestContext(request))

@login_required
@csrf_exempt
def confirm_email(request, key):
    """
    Endpoint to confirm you are owner of email
    """
    alt_email = Email.objects.filter(activation_key=key)
    if alt_email.exists():
        alt_email[0].confirm()
        return redirect('/')
    hero_title ="We weren't able to complete your request..."
    return renderErrorMessage(request, hero_title)

@login_required
@csrf_exempt
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
    return JSONResponse({'res':'success'})