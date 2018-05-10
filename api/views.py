import json
import re
import os

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.utils import timezone

from annoying.decorators import ajax_request

from api.defaults import DEFAULT_BLACKLIST
from api.models import EyeHistory
from api.models import MuteList
from api.models import WhiteListItem
from tags.models import Tag

from common.templatetags.gravatar import gravatar_img_for_user
from common.view_helpers import validate_url
from common.npl.date_parser import DateRangeParser

from live_stream.query_managers import history_search

import datetime

STOPWORDS = re.compile(
    "i|me|my|myself|we|us|our|ours|ourselves|you|your|yours|yourself|yourselves|he|him|his|himself|she|her|hers|herself|it|its|itself|they|them|their|theirs|themselves|what|which|who|whom|whose|this|that|these|those|am|is|are|was|were|be|been|being|have|has|had|having|do|does|did|doing|will|would|should|can|could|ought|i'm|you're|he's|she's|it's|we're|they're|i've|you've|we've|they've|i'd|you'd|he'd|she'd|we'd|they'd|i'll|you'll|he'll|she'll|we'll|they'll|isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't|doesn't|don't|didn't|won't|wouldn't|shan't|shouldn't|can't|cannot|couldn't|mustn't|let's|that's|who's|what's|here's|there's|when's|where's|why's|how's|a|an|the|and|but|if|or|because|as|until|while|of|at|by|for|with|about|against|between|into|through|during|before|after|above|below|to|from|up|upon|down|in|out|on|off|over|under|again|further|then|once|here|there|when|where|why|how|all|any|both|each|few|more|most|other|some|such|no|nor|not|only|own|same|so|than|too|very|say|says|said|shall")


@login_required
@ajax_request
def delete_eyehistory(request):
    try:
        delete_everything_domain = request.POST.get('delete_domain', False)
        user = request.user
        if delete_everything_domain:
            domain = request.POST.get('domain', '')
            e = EyeHistory.objects.filter(domain=domain, user=user)
        else:
            urls = json.loads(request.POST.get('urls', '[]'))
            e = EyeHistory.objects.filter(url__in=urls, user=user)

        e.delete()
    except Exception, e:
        return {"res": False,
                "error": e}

    return {"res": True}


@login_required
@ajax_request
def mutelist_add(request):
    user = request.user
    success = False
    errors = {}
    data = None
    _type = request.POST.get('form_type', None)

    if request.POST and request.is_ajax() and _type == "mutelist":
        url = request.POST.get('url', None)
        word = request.POST.get('word', None)

        errors['mutelist'] = []

        if url:
            data = {'url': url}
            if not validate_url(url):
                if url.strip() == "":
                    errors['mutelist'].append("Enter a url!")
                else:
                    errors['mutelist'].append("%s is not a valid url." % url)
            elif MuteList.objects.filter(url=url, user=user).exists():
                errors['mutelist'].append(
                    "You already registered the mutelist item %s" % url)

            if not len(errors['mutelist']):
                mutelist = MuteList(url=url, user=user)
                mutelist.save()
                data['id'] = mutelist.id
                success = "Added %s" % url
        elif word:
            data = {'word': word}
            if word.strip() == "":
                errors['mutelist'].append("Enter a phrase!")
            elif MuteList.objects.filter(word=word, user=user).exists():
                errors['mutelist'].append(
                    "You already registered the mutelist item %s" % word)

            if not len(errors['mutelist']):
                mutelist = MuteList(word=word, user=user)
                mutelist.save()
                data['id'] = mutelist.id
                success = "Added %s" % word

    return {
        'success': success,
        'errors': errors,
        'type': _type,
        'data': data,
    }


@login_required
@ajax_request
def whitelist_add(request):
    """
    API endpoint to add a whitelist item
    """
    user = request.user
    success = False
    errors = {}
    data = None
    _type = request.POST.get('form_type', None)

    if request.POST and request.is_ajax():

        if _type == "whitelist":
            url = request.POST.get('whitelist')
            errors['whitelist'] = []
            data = {'url': url}

            if url in DEFAULT_BLACKLIST:
                errors['whitelist'].append("Cannot whitelist this url.")
            elif not validate_url(url):
                if url.strip() == "":
                    errors['whitelist'].append("Enter a url!")
                else:
                    errors['whitelist'].append("%s is not a valid url." % url)
            elif WhiteListItem.objects.filter(url=url, user=user).exists():
                errors['whitelist'].append(
                    "You already registered the whitelist item %s" % url)

            if not len(errors['whitelist']):
                whitelist_item = WhiteListItem(url=url, user=user)
                whitelist_item.save()
                data['id'] = whitelist_item.id
                success = "Added %s" % url

    return {
        'success': success,
        'errors': errors,
        'type': _type,
        'data': data,
    }


def search_graph_data(request):
    username = request.GET.get('username', None)
    
    query = request.GET.get("query", None)
    if query == "null":
        query = None
    
    date = request.GET.get("date", None)
    if date == "null":
        date = None
    
    filter = request.GET.get("filter", None)
    if filter == "null":
        filter = None

    start_time = None
    end_time = None

    if date:
        start_time, end_time = DateRangeParser().parse(date)

    hist_type, hist = history_search(request.user, sort="time",
                                     query=query, filter=filter,
                                     username=username, start_time=start_time,
                                     end_time=end_time)
    if start_time is None:
        start_time = datetime.datetime.now()

    if end_time is None:
        end_time = datetime.datetime.now()
    return hist, start_time, end_time


def word_cloud(request):

    hist, start_time, end_time = search_graph_data(request)

    week_titles = hist.values_list('title')

    week_words = {}
    for title in week_titles:
        for word in title[0].split():
            if re.match('^[\w]+$', word) is not None:
                word = word.lower()
                if re.match(STOPWORDS, word) is None:
                    if word not in week_words:
                        week_words[word] = 1
                    else:
                        week_words[word] += 1

    return HttpResponse(json.dumps({
        'week_words': week_words.items(),
        'start_time': start_time.strftime("%Y-%m-%d"),
        'end_time': end_time.strftime("%Y-%m-%d"),
    }), content_type="application/json")


def load_js_file(request, filename):
    username = request.GET.get("username", "")
    date = request.GET.get("date", "")
    query = request.GET.get("query", "")
    filter = request.GET.get("filter", "")

    text = "var username=\"%s\";" % username
    text += "var date = \"%s\";" % date
    text += "var query = \"%s\";" % query
    text += "var filter = \"%s\";" % filter

    module_dir = os.path.dirname(__file__)
    file_path = module_dir + '/static/api/js/' + filename
    js = open(file_path, 'r').read()
    text += js

    return HttpResponse(text, content_type="application/javascript")


def word_cloud_js(request):
    return load_js_file(request, "word_cloud_boilerplate.js")


def bar_hour_js(request):
    return load_js_file(request, "bar_hour_boilerplate.js")


def bar_day_js(request):
    return load_js_file(request, "bar_day_boilerplate.js")


def timeline_hour(request):
    domain_count = request.GET.get('domain_count', 10)

    hist, start_time, end_time = search_graph_data(request)

    week_domains = hist.values('domain').annotate(
        num_domains=Sum('total_time')).order_by('-num_domains')[:domain_count]

    domain_list = [domain['domain'] for domain in week_domains]

    domain_count = len(domain_list)

    if domain_count == 10:
        week_hours = [None] * (domain_count + 1)
    else:
        week_hours = [None] * (domain_count)
    week_time = hist.values('domain', 'start_time', 'total_time')
    for w_time in week_time:

        hour = timezone.localtime(w_time['start_time']).hour

        try:
            pos = domain_list.index(w_time['domain'])
            if week_hours[pos] is None:
                week_hours[pos] = {}
            if hour not in week_hours[pos]:
                week_hours[pos][hour] = 0.0
            week_hours[pos][hour] += float(w_time['total_time']) / 60000.0
        except ValueError:
            if domain_count == 10:
                if week_hours[domain_count] is None:
                    week_hours[domain_count] = {}
                if hour not in week_hours[domain_count]:
                    week_hours[domain_count][hour] = 0.0
                week_hours[domain_count][
                    hour] += float(w_time['total_time']) / 60000.0

    for i in range(len(week_hours)):
        if week_hours[i]:
            list_hours = []
            for h in range(24):
                if h not in week_hours[i]:
                    list_hours.append({"time": h, "y": 0})
                else:
                    list_hours.append({"time": h, "y": week_hours[i][h]})
            week_hours[i] = list_hours
        else:
            week_hours[i] = [{"time": x, "y": 0} for x in range(24)]

    return HttpResponse(json.dumps({
        'week_hours': week_hours,
        'domain_list': domain_list,
        'start_time': start_time.strftime("%Y-%m-%d"),
        'end_time': end_time.strftime("%Y-%m-%d"),
    }), content_type="application/json")


def timeline_day(request):
    domain_count = request.GET.get('domain_count', 10)
    hist, start_time, end_time = search_graph_data(request)

    week_domains = hist.values('domain').annotate(
        num_domains=Sum('total_time')).order_by('-num_domains')[:domain_count]

    domain_list = [domain['domain'] for domain in week_domains]

    domain_count = len(domain_list)

    week_time = hist.values('domain', 'start_time', 'total_time')

    if domain_count == 10:
        week_days = [None] * (domain_count + 1)
    else:
        week_days = [None] * (domain_count)
    for w_time in week_time:

        day = timezone.localtime(w_time['start_time']).weekday()

        try:
            pos = domain_list.index(w_time['domain'])
            if week_days[pos] is None:
                week_days[pos] = {}
            if day not in week_days[pos]:
                week_days[pos][day] = 0.0
            week_days[pos][day] += float(w_time['total_time']) / 60000.0
        except ValueError:
            if domain_count == 10:
                if week_days[domain_count] is None:
                    week_days[domain_count] = {}
                if day not in week_days[domain_count]:
                    week_days[domain_count][day] = 0.0
                week_days[domain_count][
                    day] += float(w_time['total_time']) / 60000.0

    for i in range(len(week_days)):
        if week_days[i]:
            list_days = []
            for d in range(7):
                if d not in week_days[i]:
                    list_days.append({"time": d, "y": 0})
                else:
                    list_days.append({"time": d, "y": week_days[i][d]})
            week_days[i] = list_days
        else:
            week_days[i] = [{"time": x, "y": 0} for x in range(7)]

    return HttpResponse(json.dumps({
        'week_days': week_days,
        'domain_list': domain_list,
        'start_time': start_time.strftime("%Y-%m-%d"),
        'end_time': end_time.strftime("%Y-%m-%d"),
    }), content_type="application/json")


@ajax_request
def my_tags(request):
    if request.user.is_authenticated():
        t = list(
            set(Tag.objects.filter(
                user=request.user
            ).values_list('name', 'color')))
        return {'tags': t}
    return {'tags': None}


@ajax_request
def typeahead(request):
    query = request.GET.get('query', None)
    success = False
    errors = "no query"
    users = None

    if query:
        users = {}
        terms = query.split()
        for term in terms:
            filtered_users = User.objects.filter(
                Q(username__istartswith=term) |
                Q(email__istartswith=term, userprofile__anon_email=False) |
                Q(first_name__istartswith=term) |
                Q(last_name__istartswith=term)
            )
            if filtered_users.exists():
                for user in filtered_users:
                    users[user.id] = {
                        'username': user.username,
                        'fullname': user.get_full_name(),
                        'email': user.email,
                        'gravatar': gravatar_img_for_user(user, 24)
                    }

        if not len(users):
            errors = 'no match. query: %s' % query
            users = None
        else:
            errors = None
            success = True
            users = users.values()

    res = {
        'success': success,
        'errors': errors,
        'users': users
    }

    return res
