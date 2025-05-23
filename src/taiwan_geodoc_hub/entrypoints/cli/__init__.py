from typer import Typer
from click.core import Context
from taiwan_geodoc_hub.infrastructure.utils.event_loop import ensure_event_loop
from taiwan_geodoc_hub.infrastructure.lifespan import startup, shutdown
from atexit import register
from taiwan_geodoc_hub.entrypoints.cli.auth import auth

app = Typer()


@app.callback()
def bootstrap(context: Context):
    loop = ensure_event_loop()
    context.obj = loop.run_until_complete(startup())
    register(lambda: loop.run_until_complete(shutdown()))


app.add_typer(auth)
