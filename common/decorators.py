from functools import wraps
from django.utils.decorators import available_attrs
from common.view_helpers import NotImplementedResponse

def assert_post_request(request):
    """
    Decorator for views that checks that checks if the request is a post request and sends return a NotImplemented if not.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'POST':
                return view_func(request, *args, **kwargs)
            return NotImplementedResponse()
            
        return _wrapped_view
    return decorator