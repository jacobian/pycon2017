# Closing Thoughts

---

### This is a web framework, all the rest is commentary

Really: what you've seen today make up the fundamental building blocks of a web framework. Everything else builds on top of these components.

---

### Example: authentication

An authentication system is:

- Cookie handling (WSGI and the request/response abstraction)
- A session abstraction (cookies + data storage)
- User abstractions (sessions + data storage)
- Controllers for login, logout, registration, etc (users + routing, controllers, templates)

---

### Should you use what you built today in production?

<p class="stretch"><img class="fragment" src="img/nope.gif" height="100%" width="100%"></p>

---

### Should you build a new web framework?


Probably not: Python's got a few **really** good ones.

But maybe yes: certain choices (request/response, ORMs, templates) are starting to look pretty outdated.

And, of course, "reinventing the wheel is great if your goal is to learn more about wheels." 
<!-- .element: class="fragment" -->

---

# Thank you!

Jacob Kaplan-Moss

[jacob@jacobian.org](mailto:jacob@jacobian.org)

Feedback? https://www.surveymonkey.com/r/pycon250 
