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
