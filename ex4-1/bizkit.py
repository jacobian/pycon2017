import http.client
import importlib
import os
import re
import sys
import urllib.parse
from wsgiref.headers import Headers
from wsgiref.simple_server import make_server

class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def args(self):
        get_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
        return {k:v[0] for k, v in get_args.items()}

    @property
    def path(self):
        return self.environ['PATH_INFO']

class Response:
    def __init__(self, response=None, status=200, charset='utf-8', content_type='text/html'):
        if response is None:
            self.response = []
        elif isinstance(response, (str, bytes)):
            self.response = [response]
        else:
            self.response = response
            
        self.charset = charset
        self.headers = Headers()
        self.headers.add_header('content-type', f'{content_type}; charset={charset})')
        self._status = status

    @property
    def status(self):
        status_string = http.client.responses.get(self._status, 'UNKNOWN STATUS')
        return f'{self._status} {status_string}'

    def __iter__(self):
        for k in self.response:
            if isinstance(k, bytes):
                yield k
            else:
                yield k.encode(self.charset) 

class NotFound(Exception):
    pass

class Router:
    def __init__(self):
        self.routing_table = []

    def add_route(self, pattern, callback):
        self.routing_table.append((pattern, callback))

    def match(self, path):
        for (pattern, callback) in self.routing_table:
            m = re.match(pattern, path)
            if m:
                return (callback, m.groups())
        raise NotFound()

def application(environ, start_response):
    module = os.environ['BIZKIT_APP']
    module = importlib.import_module(module)
    router = getattr(module, 'routes')

    try:
        request = Request(environ)
        callback, args = router.match(request.path)
        response = callback(request, *args)
    except NotFound:
        response = Response("<h1>Not found</h1>", status=404)

    start_response(response.status, response.headers.items())
    return iter(response)

if __name__ == '__main__':
    with make_server('', 5000, application) as server:
        server.serve_forever()
