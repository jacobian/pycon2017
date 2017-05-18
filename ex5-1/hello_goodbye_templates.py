from bizkit import TemplateResponse, Router

def hello(request, name):
    context = {"greeting": "Hello", "name": name}
    return TemplateResponse("greeting.html", context)

def goodbye(request, name):
    context = {"greeting": "Goodbye", "name": name}
    return TemplateResponse("greeting.html", context)

routes = Router()
routes.add_route(r'/hello/(.*)/$', hello)
routes.add_route(r'/goodbye/(.*)/$', goodbye)
