from django import http
from django.conf import settings

XS_SHARING_ALLOWED_ORIGINS = getattr(settings, 'XS_SHARING_ALLOWED_ORIGINS', '*')
XS_SHARING_ALLOWED_HEADERS = getattr(settings, 'XS_SHARING_ALLOWED_HEADERS', ['Content-type'])

XS_SHARING_ALLOWED_METHODS = getattr(settings, 'XS_SHARING_ALLOWED_METHODS', ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE'])

XS_SHARING_ALLOWED_CREDENTIALS = getattr(settings, 'XS_ALLOW_CREDENTIALS', True)

class XsSharing(object):
    """
    This middleware allows cross-domain XHR using the html5 postMessage API.
     
    Access-Control-Allow-Origin: http://foo.example
    Access-Control-Allow-Methods: POST, GET, OPTIONS, PUT, DELETE

    Based off https://gist.github.com/426829
    """
    def process_request(self, request):
        if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in request.META:
            return self.fill_response()

        return None

    def process_response(self, request, response):
        return self.fill_response(response)

    def fill_response(self, response=None):
        if not response:
            response = http.HttpResponse()
        response['Access-Control-Allow-Origin']  = XS_SHARING_ALLOWED_ORIGINS 
        response['Access-Control-Allow-Methods'] = ", ".join( XS_SHARING_ALLOWED_METHODS )
        response['Access-Control-Allow-Headers'] = ", ".join( XS_SHARING_ALLOWED_HEADERS )
        response['Access-Control-Allow-Credentials'] = XS_SHARING_ALLOWED_CREDENTIALS
        return response