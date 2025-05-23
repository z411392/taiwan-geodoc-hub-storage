from starlette.requests import Request
from starlette.responses import JSONResponse


async def on_checking_health(request: Request):
    return JSONResponse(
        dict(
            success=True,
            data=dict(),
        )
    )
