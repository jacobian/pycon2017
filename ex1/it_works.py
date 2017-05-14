from wsgiref.simple_server import make_server, demo_app

if __name__ == '__main__':
    with make_server('', 5000, demo_app) as server:
        server.serve_forever()