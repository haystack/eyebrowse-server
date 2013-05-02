"""
    Generic view helpers live here.
"""
from django.shortcuts import HttpResponse
from django.utils import simplejson as json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

from common.npl.date_parser import DateRangeParser


def JSONResponse(payload):
    """
    Helper to return HttpResponse with json type
    json.dumps the payload given
    """
    return HttpResponse(json.dumps(payload), mimetype='application/json')

def NotImplementedResponse():
    return JSONResponse({'error':"NotYetImplemented"})

def _template_values(request, page_title='', navbar='', sub_navbar='', **kwargs):
    template_values = {
        'page_title' : page_title,
        navbar : 'active',
        sub_navbar : 'active',
        'user' : request.user,
    }

    return dict(template_values.items() + kwargs.items())

def _get_query(request):
    """
        Get query parameters if search is used
    """
    query = request.GET.get("query", "")
    date = request.GET.get("date", "")
    start_time = None
    end_time = None
    
    if date:
        start_time, end_time = DateRangeParser().parse(date)

    get_dict = {
        "query" : query,
        "filter" : request.GET.get("filter", "following"),
        "start_time" : start_time,
        "end_time": end_time,
        "username" : request.GET.get("username", ""),
        "orderBy" : request.GET.get("orderBy", "start_time"),
        "direction" : request.GET.get("direction", ""),
        "template" : request.GET.get("template", ""),
    }
    
    return get_dict, query, date


def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validate_url(url):
    if not url.count('://'):
        url = "http://" + url
    validate = URLValidator(verify_exists=True)
    try:
        validate(url)
        return True
    except ValidationError, e:
        return False