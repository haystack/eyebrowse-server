import random

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

from annoying.decorators import ajax_request
from annoying.decorators import render_to

from accounts.models import UserProfile

from api.models import WhiteListItem
from tags.models import Tag
from stats.models import MoralData

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

@render_to('common/tutorial.html')
def tutorial(request):
    return _template_values(request)


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


@csrf_exempt
@login_required
@ajax_request
def delete_tag(request):
    domain = request.POST.get('domain', None)
    name = request.POST.get('tag', None)
    page_url = request.POST.get('url', None)

    user = request.user

    if domain and name:
        tags = Tag.objects.filter(user=user, domain=domain, name=name)
        tags.delete()
    elif name and page_url:
        tags = Tag.objects.filter(user=user, common_tag__name=name, page__url=process_url(page_url))
        tags.delete()
    elif name:
        tags = Tag.objects.filter(user=user, name=name)
        tags.delete()

    return {'res': 'success'}


@render_to('google3a0cf4e7f8daa91b.html')
def google_verify(request):
    return {}

@login_required
@render_to('common/mft_results_827.html')
def mft_results_treatment(request):
    auth = 0
    loy = 0
    fair = 0
    care = 0
    pure = 0
    user = request.user

    if request.POST:
        a1 = int(request.POST.get("a1")[0]) # auth
        b1 = int(request.POST.get("b1")[0]) # ???
        c1 = int(request.POST.get("c1")[0]) # loy
        d1 = int(request.POST.get("d1")[0]) # care
        e1 = int(request.POST.get("e1")[0]) # fair
        f1 = int(request.POST.get("f1")[0]) # pure
        g1 = int(request.POST.get("g1")[0]) # loy
        q1 = int(request.POST.get("q1")[0]) # loy
        i1 = int(request.POST.get("i1")[0]) # auth
        j1 = int(request.POST.get("j1")[0]) # care
        k1 = int(request.POST.get("k1")[0]) # care
        l1 = int(request.POST.get("l1")[0]) # pure
        m1 = int(request.POST.get("m1")[0]) # auth
        n1 = int(request.POST.get("n1")[0]) # fair
        o1 = int(request.POST.get("o1")[0]) # fair
        p1 = int(request.POST.get("p1")[0]) # pure 

        a2 = int(request.POST.get("a2")[0]) # auth
        b2 = int(request.POST.get("b2")[0]) # care
        c2 = int(request.POST.get("c2")[0]) # auth
        d2 = int(request.POST.get("d2")[0]) # pure
        e2 = int(request.POST.get("e2")[0]) # fair
        f2 = int(request.POST.get("f2")[0]) # care
        g2 = int(request.POST.get("g2")[0]) # auth
        q2 = int(request.POST.get("q2")[0]) # loy
        i2 = int(request.POST.get("i2")[0]) # pure 
        j2 = int(request.POST.get("j2")[0]) # pure
        k2 = int(request.POST.get("k2")[0]) # fairn
        l2 = int(request.POST.get("l2")[0]) # loy
        m2 = int(request.POST.get("m2")[0]) # fair
        n2 = int(request.POST.get("n2")[0]) # care
        o2 = int(request.POST.get("o2")[0]) # pure
        p2 = int(request.POST.get("p2")[0]) # loy

        auth = float(a1 + i1 + m1 + a2 + c2 + g2) / 6.0
        loy = float(c1 + g1 + q1 + q2 + l2 + p2) / 6.0
        care = float(d1 + j1 + k1 + b2 + f2 + n2) / 6.0
        fair = float(e1 + n1 + o1 + e2 + k2 + m2) / 6.0
        pure = float(f1 + l1 + p1 + d2 + i2 + j2) / 6.0

        m = MoralData(authority=auth, loyalty=loy, care=care, fairness=fair, purity=pure, user=user, is_treatment=True)
        m.save()

    else:
        try:
            m = MoralData.objects.get(user=user)
            auth = m.authority
            loy = m.loyalty
            fair = m.fairness
            pure = m.purity
            care = m.care
        except:
            pass

    return _template_values(request,
                            page_title="Moral Questionnaire Results", authority=auth, loyalty=loy, fairness=fair, care=care, purity=pure);
@login_required
@render_to('common/mft_results_543.html')
def mft_results_control(request):
    auth = 0
    loy = 0
    fair = 0
    care = 0
    pure = 0
    user = request.user

    if request.POST:
        a1 = int(request.POST.get("a1")[0]) # auth
        b1 = int(request.POST.get("b1")[0]) # ???
        c1 = int(request.POST.get("c1")[0]) # loy
        d1 = int(request.POST.get("d1")[0]) # care
        e1 = int(request.POST.get("e1")[0]) # fair
        f1 = int(request.POST.get("f1")[0]) # pure
        g1 = int(request.POST.get("g1")[0]) # loy
        q1 = int(request.POST.get("q1")[0]) # loy
        i1 = int(request.POST.get("i1")[0]) # auth
        j1 = int(request.POST.get("j1")[0]) # care
        k1 = int(request.POST.get("k1")[0]) # care
        l1 = int(request.POST.get("l1")[0]) # pure
        m1 = int(request.POST.get("m1")[0]) # auth
        n1 = int(request.POST.get("n1")[0]) # fair
        o1 = int(request.POST.get("o1")[0]) # fair
        p1 = int(request.POST.get("p1")[0]) # pure 

        a2 = int(request.POST.get("a2")[0]) # auth
        b2 = int(request.POST.get("b2")[0]) # care
        c2 = int(request.POST.get("c2")[0]) # auth
        d2 = int(request.POST.get("d2")[0]) # pure
        e2 = int(request.POST.get("e2")[0]) # fair
        f2 = int(request.POST.get("f2")[0]) # care
        g2 = int(request.POST.get("g2")[0]) # auth
        q2 = int(request.POST.get("q2")[0]) # loy
        i2 = int(request.POST.get("i2")[0]) # pure 
        j2 = int(request.POST.get("j2")[0]) # pure
        k2 = int(request.POST.get("k2")[0]) # fairn
        l2 = int(request.POST.get("l2")[0]) # loy
        m2 = int(request.POST.get("m2")[0]) # fair
        n2 = int(request.POST.get("n2")[0]) # care
        o2 = int(request.POST.get("o2")[0]) # pure
        p2 = int(request.POST.get("p2")[0]) # loy

        auth = float(a1 + i1 + m1 + a2 + c2 + g2) / 6.0
        loy = float(c1 + g1 + q1 + q2 + l2 + p2) / 6.0
        care = float(d1 + j1 + k1 + b2 + f2 + n2) / 6.0
        fair = float(e1 + n1 + o1 + e2 + k2 + m2) / 6.0
        pure = float(f1 + l1 + p1 + d2 + i2 + j2) / 6.0

        m = MoralData(authority=auth, loyalty=loy, care=care, fairness=fair, purity=pure, user=user)
        m.save()


    return _template_values(request,
                            page_title="Moral Questionnaire Results");

@login_required
def mft(request, token=None):
    user = request.user
    part_one = {
        "Whether or not someone conformed to the traditions of society.": "a1",
        "Whether or not someone was good at math.": "b1",
        "Whether or not someone showed a lack of loyalty.": "c1",
        "Whether or not someone was cruel.": "d1",
        "Whether or not some people were treated differently than others.": "e1",
        "Whether or not someone did something disgusting.": "f1",
        "Whether or not someone did something to betray his or her group.": "g1",
        "Whether or not someone's action showed love for his or her country.": "q1",
        "Whether or not someone showed a lack of respect for authority.": "i1",
        "Whether or not someone cared for someone weak or vulnerable.": "j1",
        "Whether or not someone suffered emotionally.": "k1",
        "Whether or not an action caused chaos or disorder.": "l1",
        "Whether or not someone acted in a way that God would approve of.": "m1",
        "Whether or not someone was denied his or her rights.": "n1",
        "Whether or not someone acted unfairly.": "o1",
        "Whether or not someone violated standards of purity and decency.": "p1",
    }

    part_two = {
        "If I were a soldier and disagreed with my commanding officer's orders, I would obey anyway because that is my duty.": "a2",
        "Compassion for those who are suffering is the most crucial virtue.": "b2",
        "Respect for authority is something all children need to learn.": "c2",
        "Chastity is an important and valuable virtue.": "d2",
        "Justice is the most important requirement for a society.": "e2",
        "It is better to do good than to do bad.": "f2", 
        "Men and women each have different roles to play in society.": "g2",
        "I am proud of my country's history.": "q2",
        "People should not do things that are disgusting, even if no one is harmed.": "i2",
        "I would call some acts wrong on the grounds that they are unnatural.": "j2",
        "I think it's morally wrong that rich children inherit a lot of money while poor children inherit nothing.": "k2",
        "It is more important to be a team player than to express oneself.": "l2",
        "When the government makes laws, the number one principle should be ensuring that everyone is treated fairly.": "m2",
        "One of the worst things a person could do is hurt a defenseless animal.": "n2",
        "It can never be right to kill a human being.": "o2",
        "People should be loyal to their family members, even when they have done something wrong.": "p2",

    }

    q1_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for q in part_one:
        rand = random.randint(0, 15)
        while q1_array[rand] != 0:
            rand = random.randint(0, 15)

        q1_array[rand] = {'question': q, 'class': part_one[q]}

    q2_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for q in part_two:
        rand = random.randint(0, 15)
        while q2_array[rand] != 0:
            rand = random.randint(0, 15)

        q2_array[rand] = {'question': q, 'class': part_two[q]}

    try:
        md_objs = MoralData.objects.filter(user=user)
        m = md_objs[len(md_objs) - 1]
	if m.is_treatment:
            return render(request, 'common/mft_results_827.html',
                            {'authority':m.authority, 'loyalty':m.loyalty, 'care':m.care, 'fairness':m.fairness, 'purity':m.purity});
        else:
            return render(request, 'common/mft_results_543.html');
    except:
        pass

    return render(request, 'common/mft.html', {
            'token': token,
            'part_one': q1_array, 
            'part_two': q2_array,
        })

    # context_instance=RequestContext(request)

    # return ren(request,
    #                         page_title="Your Morals", token=token, part_one=q1_array, part_two=q2_array, )


# Helper function to parse urls minus query strings
def process_url(url):
  for i in range(len(url)):
    if url[i] == "?":
      return url[:i]

  return url
