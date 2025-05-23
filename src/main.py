from firebase_functions.https_fn import on_request
from taiwan_geodoc_hub.entrypoints.http.starlette import (
    vellox as handle_request,
)
from taiwan_geodoc_hub.infrastructure.utils.event_loop import ensure_event_loop
from async_typer import AsyncTyper
from taiwan_geodoc_hub.entrypoints.cli.auth import app as auth
from dotenv import load_dotenv
from os.path import exists


@on_request()
def upload(request):
    ensure_event_loop()
    return handle_request(request)


if __name__ == "__main__":
    loop = ensure_event_loop()
    if exists("src/.env"):
        load_dotenv("src/.env", override=True)
    app = AsyncTyper()
    app.add_typer(auth)
    loop.run_until_complete(app())
