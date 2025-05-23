from typer import Typer
from click.core import Context
from taiwan_geodoc_hub.infrastructure.utils.event_loop import ensure_event_loop
from taiwan_geodoc_hub.modules.access_managing.presentation.cli.login import (
    login as login_async,
)

auth = Typer(name="auth")


@auth.command()
def login(context: Context):
    loop = ensure_event_loop()
    return loop.run_until_complete(login_async(context))
