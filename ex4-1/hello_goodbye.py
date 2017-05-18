from bizkit import Response, Router

def hello(request, name):
    return Response(f"<h1>Hello, {name}</h1>")

def goodbye(request, name):
    return Response(f"<h1>Goodbye, {name}</h1>")

routes = Router()
routes.add_route(r'/hello/(.*)/$', hello)
routes.add_route(r'/goodbye/(.*)/$', goodbye)
