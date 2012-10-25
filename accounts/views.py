from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from common.models import *
from common.view_helpers import _template_values, JSONResponse


@login_required
def profile(request, username=None):
    """
        User profile page
    """
    if not username:
        username = request.user.username

    profile_user = get_object_or_404(User, username=username)

    template_values = _template_values(request, nav_bar='nav_profile', profile_user=profile_user)

    return render_to_response('accounts/profile.html', template_values, context_instance=RequestContext(request))

@login_required
def edit_profile(request):
    """
    Edit profile page
    """

    user = request.user
    profile = user.profile

    template_values = _template_values(request, nav_bar='nav_account')

    return render_to_response('accounts/edit_profile.html', template_values, context_instance=RequestContext(request))