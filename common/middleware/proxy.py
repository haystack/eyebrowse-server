import requests

from urlparse import urlparse

from django.utils import simplejson as json
from django.http import HttpResponse


REQUEST_MAP = {
    "GET": requests.get,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete
}

COOKIE_KEYS = ["csrftoken", "sessionid"]
HEADER_KEYS = ["Content-Type"]
IGNORED_ARGS = set(["proxy_url"] + COOKIE_KEYS + HEADER_KEYS)
IGNORE_HEADERS = ["Origin", "User-Agent", "Host"]
ALLOWED_NETLOC = set([
    "eyebrowse.csail.mit.edu",
    "localhost:8000"
])
LOGIN = "login"


class ProxyMiddleware(object):

    """
    Takes cookie and sessionid values of
    request and creates actual django cookies
    """

    def process_request(self, request):
        return _process(request)


def _process(request):
    params = request.GET
    proxy_url = None

    if len(params) > 0:
        proxy_url = params.get("proxy_url")

    if proxy_url:
        method = request.method
        netloc = urlparse(proxy_url).netloc

        if netloc not in ALLOWED_NETLOC:
            return _err_response(
                "Invalid proxy url provided, must foward to eyebrowse.")

        if method not in REQUEST_MAP:
            return _err_response("Invalid request method type %s" % method)

        request_dict = _pack_request(request)
        res = REQUEST_MAP[method](proxy_url, **request_dict)
        res = _pack_response(res)
        response = HttpResponse(res['response'])

        if LOGIN in proxy_url:
            val = ''
            try:
                json_res = json.loads(res['response'])
            except:
                return _err_response("JSON decode error.")

            for key, value in json_res.iteritems():
                if key == 'sessionid':
                    val = value
            response.set_cookie('sessionid', val)
        return response

    return None


def _pack_request(request):
    """
        Builds a dictionary of options to send with the request
    """
    cookies = _extract_cookies(request.GET)  # extract cookies to proxy
    headers = _extract_headers(request.META)
    if request.method == "GET":
        args_key = "params"
        args = _clean_args(request.GET)
    else:
        args_key = "data"
        args = request.POST
    return {
        "cookies": cookies,
        args_key: args,
        "headers": _pack_headers(request, headers),
        "allow_redirects": True
    }


def _err_response(err_msg):
    return {
        'error': err_msg
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
    for k, v in arg_dict.iteritems():
        if k not in IGNORED_ARGS:
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
        res = res.history[0]  # login redirect
        if res.request.method == "POST" and res.status_code == 302:
            # we just want to save cookies for logging in
            response = json.dumps(res.cookies.get_dict())
            content_type = "application/json; charset=utf-8"
    else:
        try:
            response = json.dumps(res.json())
        except:
            response = res.text

    return {
        "content_type": content_type,
        "response": response
    }
