from django.views.decorators.clickjacking import xframe_options_exempt

from annoying.decorators import render_to

@xframe_options_exempt
@render_to("extension/prompt.html")
def prompt(request):
    site = request.GET.get("site", '')
    return {
        'site' : site
    }