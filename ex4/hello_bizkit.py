from bizkit import Response

def hello(request):
    name = request.args.get('name', 'PyCon')
    return Response(f"<h1>Hello, {name}</h1>")