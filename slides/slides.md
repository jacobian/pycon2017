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

## What's a web framework?

xxx

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
- Know how to run WSGI apps in a couple of different ways

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

    - introduce WSGI, handler, etc
    - ex2: write a wsgi app
        - objective: understand wsgi (a bit), write an app by hand
        - html, "hello pycon'"
        - show output, don't show how
        - hint: could start by replacing demo_app
        - bonus: add ?name=foo support (will require fucking with unicode!)

---

# Part 3: Request/response abstractions

    - wsgi app sucks (see above w/unicode!)
    - request/response abstraction as response
        - where it breaks down (websockets, http2)
    - ex3: write request/response abstraction
        - objective: understand wrappers, parsing wsgi env, etc
        - show: final code, decorator,nothing else
    - after: show code, talk about all the ways it breaks
    - show werkzeug version, compare a few things
    - admission: in many ways, we're building a really shitty werkzeug
    - DECISION POINT: by-hand vs werkzeug
        - if you want to struggle, keep doing things by hand
        - if you want the exercises to be easy, keep using werkzeug
        - if I were building Django from scratch today, I'd use werkzeug

- Let's make this a framework
    - framework vs lib
        - thinking about entry points
        - is Flask a framework?
    - the initial startup: how does a framework/library know what to run?
        - Flask-style: run the app!
        - Django-style: what the heck to run?
            - DJANGO_SETTINGS_MODULE oh now I get it
    - DECISION POINT: framework or library
    - ex4: do a framework, or a library
        - objective: think about the above
        - figure out entry points
        - goal: shuold have a framework/lib, and your app alone (which imports), and be able to invoke it
    - my solution: introducing bizkit
        - (django's a great mucisin, limp bizkit was named the 3rd worst band of the 90s by rolling stone) 

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
