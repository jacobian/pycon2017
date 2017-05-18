
# Part 3: Request/response abstractions

---

## Most frameworks abstract WSGI

WSGI is complex and subtle; so is HTTP. For example, this has about six bugs in it:

```python
GET = urllib.parse.parse_qs(environ['QUERY_STRING'])
name = GET.get('name', ['PyCon'])[0]
```

More to the point, WSGI is too low a level of abstraction for most practice web development purposes. So most frameworks abstract WSGI.

---

## The request/response abstraction

Most frameworks end up with a request/response abstraction, turning apps into something like:

```python
from somewhere import Response

def application(request):
    ...
    return Response('...')
```

---

## Why use the request/response pattern?

- Conceptual simplicity and elegance
- Maps closely to HTTP
- Mocking/testing can be done fairly easily
- A widely used pattern, both in Python and elsewhere

---

## Problems with the request/response pattern

- WSGI is *not* request/response, and so the abstraction leaks
- Streaming responses can be difficult
- Maps very poorly to newer web standards (HTTP2, Websockets)

---

## Exercise 3: request/response

### Goal

Understand how web frameworks map WSGI to request/response objects.

---

## Exercise 3: request/response

Write your own request/response objects, and convert your "Hello PyCon" app to use these abstractions:

```python
class Request: ...
class Response: ...

def request_response_application(function):
    def application(environ, start_response):
        ...
    return application

@request_response_application
def application(request):
    ...
    return Response(...)
```

---

## Exercise 3: My Request object

```python
import urllib.parse

class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def args(self):
        get_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
        return {k:v[0] for k, v in get_args.items()}
```

Note:
- overly simplistic `args`

---

## Exercise 3: My Response object

```python
import http.client
from wsgiref.headers import Headers

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

```

---

## Exercise 3: My converter function

```python
def request_response_application(function):
    def application(environ, start_response):
        request = Request(environ)
        response = function(request)
        start_response(response.status, response.headers.items())
        return iter(response)
    return application
```

---

## Exercise 3: My app

```python
@request_response_application
def application(request):
    name = request.args.get('name', 'PyCon')
    return Response([
        '<doctype html>',
        '<html>',
        f'<head><title>Hello, {name}</title></head>',
        f'<body><h1>Hello, {name}!</body>',
        '</html>',
    ])
```

---

Isn't there an easier way?

---

## Exercise 3: easy mode

```python
from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    name = request.args.get('name', 'PyCon')
    return Response(f'''
        <doctype html>
        <html>
        <head><title>Hello, {name}</title></head>
        <body><h1>Hello, {name}!</body>
        </html>
    ''', content_type='text/html')
```

In many ways, in this tutorial we're building a really crummy Werkzeug.

Note:
- if you want to struggle, keep doing things by hand
- if you want the exercises to be easy, keep using werkzeug
- if I were building Django from scratch today, I'd use werkzeug

---

# Decision Point:

## DIY vs BYO

---

## Is this a framework yet?

What's a "framework", exactly?

Note:
- it's all about who calls whom
- is Flask a framework?

---

## The framework startup problem

How does your framework know how to call into your code?

```bash
$ python start-my-awesome-framework.py
```

(Now you understand why `DJANGO_SETTINGS_MODULE` exists...)

---

# Decision Point:

## Framework or Library?

---

## Exercise 4: make a framework/library

### Goal

- Choose between library and framework-like patterns
- Refactor your code into a tiny framework/library

---

## Exercise 4: make a framework/library

For a **framework**, your app should just be:

```python
from myframework import Response

def hello(request):
    return Response(...)
```

And you'll point your WSGI server at `myframework.application`

For a **library**, your code could look similar, but you'll point your WSGI server directly at that file.

---

## Exercise 4: My app

```python
from bizkit import Response

def hello(request):
    name = request.args.get('name', 'PyCon')
    return Response(f"<h1>Hello, {name}</h1>")
```

---

## Exercise 4: My framework

```python
class Request: ...
class Response: ...

def application(environ, start_response):
    module, app_name = os.environ['BIZKIT_APP'].split(':')
    module = importlib.import_module(module)
    app = getattr(module, app_name)

    request = Request(environ)
    response = app(request)
    start_response(response.status, response.headers.items())
    return iter(response)
```

Run it:

```bash
BIZKIT_APP=hello_bizkit:hello twist web --wsgi bizkit.application
```

Note:
 -  limp bizkit: worst bad of the 90s get it? 
