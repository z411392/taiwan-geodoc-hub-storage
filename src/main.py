if __name__ == "__main__":
    from dotenv import load_dotenv
    from os.path import exists
    from os import environ
    from taiwan_geodoc_hub.entrypoints.cli import app

    environ["RUN_MODE"] = "cli"

    if exists("src/.env"):
        load_dotenv("src/.env", override=True)
    if exists("src/.env.local"):
        load_dotenv("src/.env.local", override=True)
    app()

else:
    from firebase_functions.https_fn import on_request
    from werkzeug.wrappers import Request
    from taiwan_geodoc_hub.entrypoints.http.vellox import vellox
    from taiwan_geodoc_hub.infrastructure.utils.event_loop import ensure_event_loop

    @on_request()
    def upload(request: Request):
        ensure_event_loop()
        return vellox(request)
