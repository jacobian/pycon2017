
# Let's build a web framework!

Jacob Kaplan-Moss

[jacob@jacobian.org](mailto:jacob@jacobian.org)

---

> ## "Reinventing the wheel is great if your goal is to learn more about wheels." 

> -- James Tauber

---

## Goals and Expectations

By the end of this tutorial, you should have **implemented a (very) minimal web framework**, from scratch, and be able to use it to **understand what frameworks do under the hood** and the **choices web framework authors face**.

This is an **intermediate-level, hands-on** course — expect to spend the majority of the time writing code.

---

## Logistics

**Slides**: Follow along with the slides at https://.../

**Teams**: I suggest pairing; there are some tricky bits, working in teams will make the exercises more manageable.

**Solutions**: If you want to peek at my solutions, you can find them at https://github.com/jacobian/pycon2017.

Note:
- pairing is going to make things easier for me too
- my code isn't great; focus on clarity of examples for slides, not anything else
- I made some specific choices - only stdlib, Django-like choices

---

## Agenda

1. Introduction & Getting Started
1. WSGI
1. HTTP request/response abstractions
1. Routing
1. Controllers, Views and Templates
1. Data storage
1. Closing thoughts

---

# Part 1: Introduction

---

## Choices web framework make

- "Do It Yourself" or "Best Of Breed"?
- Pure-WSGI or higher-level abstractions? What about Websockets? HTTP2?
- Framework or Library?
- Path-based or object-based routing?
- MVC? MTV? WTF? BBQ?
- Front-end or server-side templates?
- ... 

---

## Choices web frameworks make

There really aren't any right answers!

You'll get to make many of these choices as we work through the tutorial. By doing so, my hope is that this'll help you better understand the choices _your_ framework of choice makes.

For rather obvious reasons, _I_ will be making very similar choices to the ones Django makes. But you can -- and should -- make different ones.

---

## Where we're going

xxx

---

## Exercise 1: "It Works!"

### Goal:

- Make sure you're all set up to do future exercises.
- Know how to run WSGI apps in a couple of different ways.

---

## Exercise 1: "It works!"

1. Put this code in a file (`ex1/it_works.py`):

    ```python
    from wsgiref.simple_server import make_server, demo_app

    if __name__ == '__main__':
        with make_server('', 5000, demo_app) as server:
            server.serve_forever()
    ```

2. Run it: 

    ```sh
    $ python ex1/it_works.py
    ```

3. Try a bonafide WSGI server, e.g. Twisted, uWSGI, Waitress, Gunicorn, ...

---

## Exercise 1: My Solution

I used Twisted:

```
pip install twisted
PYTHONPATH=ex1/ twist web --wsgi it_works.demo_app
```

---

# Part 2: WSGI

---

## What is WSGI?

The Web Server Gateway Interface, defined by PEP 3333.

WSGI defines standard API for web servers (e.g. Gunicorn, uWSGI, Twisted, etc.) to connect and talk to web applications/framworks (Django, Flask, etc.). WSGI is why you can use any web server with any web application.

---

## The WSGI API

The WSGI API is desceptively simple:

`application(environ, start_response)`

- `application` is your WSGI app, a callable.
- It takes two arguments:
    - `environ`, a dict containing the WSGI envronment
    - `start_response`, a callback you call to begin the WSGI response
- Your callable returns an iterator containing the body of the response.

---

## Hello, WSGI

```python
def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/html; charset=utf8')]
    start_response(status, headers)
    return [b"<h1>Hello, World!</h1>"]
```

---

## The WSGI environ

A dict provided by the WSGI server. There are some standard keys, defined by PEP 3333, but different web servers might do things differently. Typically, keys in ALL_CAPS correspond to their CGI equivalents, and keys beginning with `wsgi.` are defined by PEP 333.

Tip: `wsgiref.simple_server.demo_app` dumps the WSGI environ:

```bash
$ twist web --wsgi wsgiref.simple_server.demo_app
```

---

## Some useful environ keys

| Key | Contents |
| --- | --- |
| `PATH_INFO` | Path component of the request, e.g. `/foo/bar/` |
| `QUERY_STRING` | GET query, e.g. `foo=bar&baz=spam` |
| `HTTP_{HEADER}` | Contents of the HTTP header `{HEADER}` |
| `wsgi.input` | xxx is this where POST lives? |

---

## The start response callable

Takes two arguments:

- `status`, a string (wat) containing the status code and readable description
- `headers`, a list of 2-tuples containing HTTP headers
    - NB: being explicit about the `charset` here is more important than you might think.

---

## The application return value

WSGI applications return iterables that yield bytes:

```python
def app(environ, start_response):
    ...
    return [b'Hello', b'World']

def app(environ, start_response):
    ...
    yield b'Hello'
    yield b'World'
```

**Make sure the charset matches what's in your `Content-Type`, or you're gonna have a bad time.**

---

## Running a WSGI app

With the standard library:

```python
if __name__ == '__main__':
    with make_server('', 5000, application) as server:
        server.serve_forever()
```

With some a WSGI server:

```
$ waitress-serve path.to.wsgi:application
$ twist web --wsgi path.to.wsgi.application
$ gunicorn path.to.wsgi:application
```

---

## Exercise 2: Hello, PyCon!

### Goal

- Understand WSGI (a bit) by hand-writing a WSGI app.
- Start to experience some of the pain that drives people to write frameworks!

---

## Exercise 2: Hello, PyCon!

1. Write an app that displays "Hello, PyCon" (in HTML)

2. Make the app support a `name` GET argument, so that `http://localhost:8080/?name=Jacob` displays "Hello, Jacob".
    - Hint: `environ['QUERY_STRING']` will be useful.
    - Hint: think carefully about unicode vs bytes!

---

## Exercise 2: My Solution

```python
import urllib.parse

def application(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/html; charset=utf-8'),
    ]
    start_response(status, headers)

    GET = urllib.parse.parse_qs(environ['QUERY_STRING'])
    name = GET.get('name', ['PyCon'])[0]

    return [
        b'<html>',
        (f'<body><h1>Hello, {name}!</body>').encode('utf-8'),
        b'</html>',
    ]
```

Note:
- unicode
- error handling
- query parsing
- mixing "application" with "view"

---

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

---

# Part 4: Routing

---

# Part 5: Controllers, Views, and Templates

---

# Part 6: Data Storage

---

# Closing Thoughts

---

# Thank you!

Jacob Kaplan-Moss

[jacob@jacobian.org](mailto:jacob@jacobian.org)
