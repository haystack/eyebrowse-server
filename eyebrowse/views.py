import random

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.models import Q

from annoying.decorators import ajax_request
from annoying.decorators import render_to

from accounts.models import UserProfile

from api.models import WhiteListItem
from tags.models import Tag

from common.admin import email_templates
from common.view_helpers import _template_values

from eyebrowse.log import logger
from django.db.models.aggregates import Count


@render_to('common/about.html')
def about(request):
    return _template_values(request,
                            page_title="Eyebrowse - About",
                            nav_about='active')


@render_to('common/faq.html')
def faq(request):
    return _template_values(request,
                            page_title="Eyebrowse - FAQ",
                            nav_faq='active')


@render_to('common/api_docs.html')
def api_docs(request):
    return _template_values(request,
                            page_title="Eyebrowse - API Docs",
                            nav_api='active')


@render_to('common/home.html')
def home(request):
    if not request.user.is_authenticated():
        return _template_values(request, page_title="home", navbar='nav_home')
    else:
        user = get_object_or_404(User, username=request.user.username)
        userprof = UserProfile.objects.get(user=user)
        confirmed = userprof.confirmed
        if not confirmed:
            return redirect('/consent')
        else:
            return redirect('/live_stream/')


@login_required
@render_to('common/consent.html')
def consent(request):
    return _template_values(request,
                            page_title="consent",
                            navbar='nav_home')


@login_required
@render_to('common/getting_started.html')
def getting_started(request):
    user_whitelist = WhiteListItem.objects.filter(
        user=request.user).values_list('url', flat=True)
    top_whitelists = WhiteListItem.objects.filter(~Q(url__in=user_whitelist)).values(
        'url').annotate(count=Count('url')).order_by('-count')[0:5]
    user_prof = UserProfile.objects.get(user=request.user)
    user_follows = list(
        user_prof.follows.all().values_list('user__username', flat=True))
    user_follows.append(request.user.username)
    top_people = UserProfile.objects.filter(~Q(user__username__in=user_follows)).annotate(
        num_followed=Count('followed_by')).order_by('-num_followed')[0:5]
    return _template_values(request, page_title="getting started", navbar='nav_home', top_whitelists=top_whitelists, top_people=top_people)


@render_to('common/downloads.html')
def downloads(request):
    return _template_values(request,
                            page_title="downloads",
                            navbar='nav_home')


@login_required
@ajax_request
def consent_accept(request):
    """
    Endpoint to submit consent
    """
    accept = request.POST.get('consent', None)
    if not accept:
        return {'res': 'failed'}

    user = get_object_or_404(User, username=request.user.username)
    prof = UserProfile.objects.get(user=user)
    prof.confirmed = True
    prof.save()
    return {'res': 'success'}


@login_required
@ajax_request
def feedback(request):
    """
    Endpoint to submit feedback
    """
    feedback = request.POST.get('feedback', None)
    if not feedback:
        return {'res': 'failed'}

    feedback.replace('\n', '<br>')
    user = request.user
    subject = email_templates.feedback['subject']
    content = email_templates.feedback['content'] % (user.username, feedback)
    admin_emails = [admin[1] for admin in settings.ADMINS]
    send_mail(subject, content, from_email=user.email,
              recipient_list=admin_emails)
    return {'res': 'success'}


@login_required
@ajax_request
def add_tag(request):
    domain = request.POST.get('domain', None)
    name = request.POST.get('tag', None)
    if not domain or not name:
        return {'res': 'failed'}

    user = request.user
    try:
        tags = Tag.objects.filter(user=user, domain=domain)
        if tags.count() > 0:
            tag = tags[0]
            tag.name = name
            tag.is_private = True
            tag.save()
        else:

            color_tags = Tag.objects.filter(user=user, name=name)
            if color_tags.count() > 0:
                color = color_tags[0].color
            else:
                r = lambda: random.randint(0, 255)
                color = '%02X%02X%02X' % (r(), r(), r())
            Tag.objects.get_or_create(
                user=user, domain=domain, name=name, color=color)
    except Exception, e:
        logger.info(e)
    return {'res': 'success'}


@login_required
@ajax_request
def color_tag(request):
    name = request.POST.get('tag', None)

    user = request.user

    tags = Tag.objects.filter(user=user, name=name)
    r = lambda: random.randint(0, 255)
    color = '%02X%02X%02X' % (r(), r(), r())

    for tag in tags:
        tag.color = color
        tag.save()
    return {'res': 'success'}


@login_required
@ajax_request
def delete_tag(request):
    domain = request.POST.get('domain', None)
    name = request.POST.get('tag', None)

    user = request.user

    if domain and name:
        tags = Tag.objects.filter(user=user, domain=domain, name=name)
        tags.delete()
    elif name:
        tags = Tag.objects.filter(user=user, name=name)
        tags.delete()

    return {'res': 'success'}


@render_to('google3a0cf4e7f8daa91b.html')
def google_verify(request):
    return {}
