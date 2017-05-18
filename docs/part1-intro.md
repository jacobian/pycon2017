
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

**Slides**: Follow along with the slides at https://github.com/jacobian/pycon2017/

**Pairing**: I suggest pairing; there are some tricky bits, working in teams will make the exercises more manageable.

**Solutions**: If you want to peek at my solutions, you can find them at https://github.com/jacobian/pycon2017

Note:
- pairing is going to make things easier for me too
- my code isn't great; focus on clarity of examples for slides, not anything else
- I made some specific choices - only stdlib, Django-like choices

---

## Agenda

1. Introduction & Getting Started
2. WSGI
3. HTTP request/response abstractions
4. Routing
5. Controllers, Views and Templates
6. Data storage
7. Closing thoughts

---

# Part 1: Introduction

---

## Choices web framework make

- "Do It Yourself" or "Best Of Breed"?
- Pure-WSGI or higher-level abstractions? What about WebSockets? HTTP2?
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

## Exercise 1-1: "It Works!"

### Goal:

- Make sure you're all set up to do future exercises.
- Know how to run WSGI apps in a couple of different ways.

---

## Exercise 1-1: "It works!"

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

## Exercise 1-1: My Solution

I used Twisted:

```
pip install twisted
PYTHONPATH=ex1/ twist web --wsgi it_works.demo_app
```
