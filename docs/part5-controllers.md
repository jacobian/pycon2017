# Part 5: Controllers, Views, and Templates

---

## Is this a good practice?

```python
def hello(request, name):
    return Response(f"<h1>Hello, {name}</h1>")

def goodbye(request, name):
    return Response(f"<h1>Goodbye, {name}</h1>")
```

---

## Separation of concerns

Most frameworks separate logic from visual presentation

Many use abstractions derived from MVC:
- **Model**: data storage, validation, data logic, etc
- **Controller**: behavior, business logic, etc
- **View**: visual presentation (i.e. HTML)

Most frameworks use a template engine as part of the view layer

Note:
- what Django calls "views" are probably better called controllers, if you're sticking to MVC

---

# Decision Point:

## Where should you render your views?

---

## Where should you render your views?

Traditionally, frameworks rendered HTML from templates on the server side.

With the rise of richer web applications, is this still a good idea?

My opinion: the next generation of web frameworks will be API-first, or API-only, with rendering done entirely client-side.

---

## Linking templates & controllers

Render in the controller and return HTML?

```python
def hello(request, name):
    t = load_template("say_hello.html")
    return Response(t.render(name=name))
```

Return the template and some data?

```python
def hello(request, name)
    return TemplateResponse("say_hello.html", name=name)
```

Specify as part of routing?

```python
@app.route("/hello/<name>", template="say_hello.html")
def hello(request, name):
    return {"name": name}
```

---

## Exercise 5-1: Use a template engine (or, don't)

1. Choose a template engine -- you probably want Jinja2.
2. Modify your controllers to use templates
    - Choose a template rendering approach that speaks to you!

Or, you know, don't -- you could make your framework API-only, and always return JSON.

Note:
- I'm going to use `string.Template` in the stdlib because I'm sticking with no-deps, but yeah

---

