from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from common.view_helpers import JSONResponse

def home(request):
    template_values = {}
    return render_to_response('common/base.html', template_values, context_instance=RequestContext(request))
