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

EXAMPLE_INVOCATIONS = {
    'ex1-1': 'twist web --wsgi it_works.demo_app --port tcp:8080',
    'ex2-2': 'twist web --wsgi simple_wsgi_app.application --port tcp:8080',
    'ex3-1': 'twist web --wsgi simple_http_objects.application --port tcp:8080',
    'ex3-2': 'BIZKIT_APP=hello_bizkit:hello twist web --wsgi bizkit.application --port tcp:8080',
    'ex4-1': 'BIZKIT_APP=hello_goodbye twist web --wsgi bizkit.application --port tcp:8080',
}

@task(name="run")
def run_example(ctx, ex):
    if not ex.startswith('ex'):
        ex = 'ex' + ex
    if ex not in EXAMPLE_INVOCATIONS:
        print(f"No such example: {ex}")
        return
    os.chdir(ex)
    ctx.run(EXAMPLE_INVOCATIONS[ex], echo=True, env={'PYTHONPATH':'.'})

slides = Collection("slides")
slides.add_task(start_slides, "start")
slides.add_task(stop_slides, "stop")

ns = Collection()
ns.add_collection(slides)
ns.add_task(run_example)
