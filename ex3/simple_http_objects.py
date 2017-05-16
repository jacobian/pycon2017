import urllib.parse
import http.client
from wsgiref.simple_server import make_server
from wsgiref.headers import Headers

def make_application(function):
    def application(environ, start_response):
        request = Request(environ)
        response = function(request)
        start_response(response.status, response.headers.items())
        return iter(response)
    return application

@make_application
def application(request):
    name = request.args.get('name', 'PyCon')
    return Response([
        '<doctype html>',
        '<html>',
        f'<head><title>Hello, {name}</title></head>',
        f'<body><h1>Hello, {name}!</body>',
        '</html>',
    ])

class Request:
    """
    An extremely simplistic HTTP request abstraction.

    Does the absolute bare minimum to get this example working, but in
    practice would break in several spectacular ways.
    """

    def __init__(self, environ):
        self.environ = environ

    @property
    def args(self):
        get_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])

        # Ignore multiple-valued keys. In practice you can't do this,
        # but it works well enough for this simple demo.
        return {k:v[0] for k, v in get_args.items()}

class Response:
    def __init__(self, response=None, status=200, charset='utf-8', content_type='text/html'):
        self.response = [] if response is None else response
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

if __name__ == '__main__':
    with make_server('', 5000, application) as server:
        server.serve_forever()