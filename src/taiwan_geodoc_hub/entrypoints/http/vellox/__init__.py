from vellox import Vellox
from taiwan_geodoc_hub.entrypoints.http.starlette import app

vellox = Vellox(
    app=app,
)
