import os
import signal
from invoke import run, task, Collection

@task
def start_slides(ctx):
    if not os.path.exists("twistd.pid"):
        ctx.run("twistd web --port tcp:5000 --path docs")

@task
def stop_slides(ctx):
    if os.path.exists("twistd.pid"):
        pid = int(open("twistd.pid").read().strip())
        os.kill(pid, signal.SIGTERM)

RUNNERS = {
    # example: (WSGI app, additional environ)
    'ex1-1': ('it_works.demo_app', {}),
    'ex2-2': ('simple_wsgi_app.application', {}),
    'ex3-1': ('simple_http_objects.application', {}),
    'ex3-2': ('bizkit.application', {'BIZKIT_APP': 'hello_bizkit:hello'}),
    'ex4-1': ('bizkit.application', {'BIZKIT_APP': 'hello_goodbye'}),
    'ex5-1': ('bizkit.application', {'BIZKIT_APP': 'hello_goodbye_templates'}),
}

@task(name="run")
def run_example(ctx, ex):
    if not ex.startswith('ex'):
        ex = 'ex' + ex
    if ex not in RUNNERS:
        print(f"No such example: {ex}")
        return

    os.chdir(ex)
    wsgi_app, env = RUNNERS[ex]
    env['PYTHONPATH'] = '.'
    ctx.run(f'twist --log-format text web --wsgi {wsgi_app} --port tcp:8080', env=env, echo=True)
    
slides = Collection("slides")
slides.add_task(start_slides, "start")
slides.add_task(stop_slides, "stop")

ns = Collection()
ns.add_collection(slides)
ns.add_task(run_example)
