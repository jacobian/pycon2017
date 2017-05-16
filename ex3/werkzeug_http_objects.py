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

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, application)