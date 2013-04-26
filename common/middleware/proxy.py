from django.utils import simplejson as json
import os
import requests
from django.http import HttpResponse

from urlparse import urlparse

REQUEST_MAP = {
    "GET" : requests.get,
    "POST" : requests.post,
    "PUT" : requests.put,
    "DELETE" : requests.delete
}

COOKIE_KEYS = ["csrftoken", "sessionid"]
HEADER_KEYS = ["Content-Type"]
IGNORED_ARGS = set(["proxy_url"] + COOKIE_KEYS + HEADER_KEYS)
IGNORE_HEADERS = ["Origin", "User-Agent", "Host"]
PROD_NETLOC = "eyebrowse.csail.mit.com"
DEV_NETLOC = "localhost:5000"

class ProxyMiddleware(object):
    """
    Takes cookie and sessionid values of request and creates actual django cookies
    """
    def process_request(self, request):
        # print "PROCESS REQUEST"
        return _process(request)

def _process(request):
    params = request.GET
    proxy_url = params.get("proxy_url")
    method = request.method
    
    if proxy_url:
        # print "FIREFOX EXTENSION"
        netloc = urlparse(proxy_url).netloc
        
        # print netloc
        if netloc != PROD_NETLOC and netloc != DEV_NETLOC:
            # print "NOT ALLOWED NETLOC"
            return {
                "error" : "Invalid proxy url provided, must foward to eyebrowse."
            }
        elif method not in REQUEST_MAP:
            # print "NOT METHOD"
            return {
                "error" : "Invalid request method type" + method
                }
        request_dict = _pack_request(request)
        res = REQUEST_MAP[method](proxy_url, **request_dict)
        res = _pack_response(res)
        response = HttpResponse(res['response'])
        response['content_type'] = res['content_type']

        if "login" in proxy_url:
            for (key,value) in json.loads(res['response']).items():
                response.set_cookie(key,value)
        for (key,value) in request.META.items():
            response.__setitem__(key,value)
        return response

    # print "LETTING IT GO TO VIEW: CHROME"
    return None

def _pack_request(request):
    """
        Builds a dictionary of options to send with the request
    """
    request_dict = {}
    cookies = _extract_cookies(request.GET) #extract cookies to proxy
    headers = _extract_headers(request.META)
    if request.method == "GET":
        args_key = "params"
        args = _clean_args(request.GET)
    else:
        args_key = "data"
        args = request.POST
    return {
        "cookies" : cookies,
        args_key : args,
        "headers" : _pack_headers(request, headers),
        "allow_redirects" : True
    }

def _extract_cookies(args):
    return _extract_args(args, COOKIE_KEYS)
def _extract_headers(args):
    return _extract_args(args, HEADER_KEYS)

def _extract_args(args, keys):
    res = {}
    for key in keys:
        if key in args:
            res[key] = args[key]
    return res

def _clean_args(arg_dict):
    """
        Take out the proxy args
    """
    clean_args = {}
    for k, v in arg_dict.items():
        if not k in IGNORED_ARGS:
            clean_args[k] = v    
    return clean_args

def _pack_headers(headers, add_headers={}):
    """
        Convert the headers from a tuple to a dictionary
    """
    header_dict = {}
    for header in headers:
        value = header[1]
        header = header[0]
        if header in IGNORE_HEADERS:
            continue
        elif header in add_headers:
            value = add_headers[header]
        header_dict[header] = value
    return header_dict

def _pack_response(res):
    """
        If we're logging in let the client get back its cookies
    """
    content_type = res.headers['content-type']
    if len(res.history):
        res = res.history[0] #login redirect
        if res.request.method == "POST" and res.status_code == 302:
            response = json.dumps(res.cookies.get_dict()) #we just want to save cookies for logging in
            content_type  = "application/json; charset=utf-8"
    else:
        try:
            response = json.dumps(res.json())
        except:
            response = res.text

    return {
        "content_type" : content_type,
        "response" : response
    }