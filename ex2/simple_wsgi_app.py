import urllib.parse
from wsgiref.simple_server import make_server

def application(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('X-Pinky', 'What are we going to do tonight, Brain?'),
    ]
    start_response(status, headers)

    GET = urllib.parse.parse_qs(environ['QUERY_STRING'])
    name = GET.get('name', ['PyCon'])[0]

    return [
        b'<doctype html>',
        b'<html>',
        (f'<head><title>Hello, {name}</title></head>').encode('utf-8'),
        (f'<body><h1>Hello, {name}!</body>').encode('utf-8'),
        b'</html>',
    ]

if __name__ == '__main__':
    with make_server('', 5000, application) as server:
        server.serve_forever()