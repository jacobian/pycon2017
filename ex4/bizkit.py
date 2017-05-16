import sys
import importlib
import urllib.parse
import http.client
from wsgiref.simple_server import make_server
from wsgiref.headers import Headers

class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def args(self):
        get_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
        return {k:v[0] for k, v in get_args.items()}

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

def make_application(function):
    def application(environ, start_response):
        request = Request(environ)
        response = function(request)
        start_response(response.status, response.headers.items())
        return iter(response)
    return application

if __name__ == '__main__':
    module, app_name = sys.argv[1].split(':')
    module = importlib.import_module(module)
    app = getattr(module, app_name)
    wrapped = make_application(app)
    with make_server('', 5000, wrapped) as server:
        server.serve_forever()

