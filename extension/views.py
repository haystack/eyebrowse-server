from django.views.decorators.clickjacking import xframe_options_exempt

from annoying.decorators import render_to

@xframe_options_exempt
@render_to("extension/track_prompt.html")
def prompt(request):
    site = request.GET.get("site", '')
    return {
        'site' : site
    }

@xframe_options_exempt
@render_to("extension/login_prompt.html")
def login(request):
    src = request.GET.get("src", "chrome")
    return {
        'src' : src
    }