"""
    Generic view helpers live here.
"""
from django.shortcuts import HttpResponse
from django.utils import simplejson as json
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def JSONResponse(payload):
    """
    Helper to return HttpResponse with json type
    json.dumps the payload given
    """
    return HttpResponse(json.dumps(payload), mimetype='application/json')

def NotImplementedResponse():
    return JSONResponse({'error':"NotYetImplemented"})

def _template_values(request, navbar='', **kwargs):
    template_values = {
        navbar : 'active',
        'user' : request.user,
    }

    return dict(template_values.items() + kwargs.items())


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