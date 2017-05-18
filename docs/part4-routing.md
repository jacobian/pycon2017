# Part 4: Routing

---

## Routing

Real apps are have many parts/functions, and Web frameworkss almost universally *route* different URLs to each function.  For example, consider Instagrm:

- `https://www.instagram.com` -- my timeline 
- `https://www.instagram.com/{username}/` -- user page for `{username}` 
- `https://www.instagram.com/p/{id}/` -- a single photo 

---

# Decision Point:

## Match-based routing, or object traversal?

---

## Object traversal

- Maps URLs to Python objects, e.g. `/user/jacob/photos/14` might map to something like `users.get("jacob").photos.get(14)`.
- Requires some sort of object routing protocol.
- Common in Python frameworks from a decade ago, but rare these days.
- Makes "reverse" resolution very difficult.
- My opinion: fell out of favor because "explicit is better than implicit"

Note:
- routing protocol: how does the framework know where to look for your `users` object? When to call `get()` vs just `getattr()`?

---

## Match-based routing

- Build a *routing table* mapping URL patterns to callables/objects. e.g., Flask:
    ```python
    @app.route("/user/<username>/photos/<int:photo_id>")
    def photo_detail(username, photo_id):
        ...
    ```
- Various options: tables vs decorators, patterns vs routes, regexes vs simpler patterns, etc.
- Most Python web frameworks do match-based routing.

---

## Exercise 4-1: write a router

1. Choose object traversal or match-based routing
2. Write two functions:
    ```python
    def hello(request): ...
    def goodbye(request): ...
    ```
3. Route `/hello` and `/goodbye` accordingly.

---

## Exercise 4-1: my app

```python
from bizkit import Response, Router

def hello(request, name):
    return Response(f"<h1>Hello, {name}</h1>")

def goodbye(request, name):
    return Response(f"<h1>Goodbye, {name}</h1>")

routes = Router()
routes.add_route(r'/hello/(.*)/$', hello)
routes.add_route(r'/goodbye/(.*)/$', goodbye)
```

---

## Exercise 4-1: my router

```python
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
```

---

### Exercise 4-1: WSGI application

```python
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
```

Note:
- small change to request to define `request.path`
- hard-coded "routes" object ugh