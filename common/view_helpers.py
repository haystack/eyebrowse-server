"""
    Generic view helpers live here.
"""

def JSONResponse(payload):
    """
    Helper to return HttpResponse with json type
    json.dumps the payload given
    """
    return HttpResponse(json.dumps(payload), mimetype='application/json')

def _template_values(request, navbar='', **kwargs):
    template_values = {
        navbar : 'active',
        'user' : request.user,
    }

    return dict(template_values.items() + kwargs.items())