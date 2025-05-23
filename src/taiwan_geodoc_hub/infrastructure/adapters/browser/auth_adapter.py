from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware

from taiwan_geodoc_hub.modules.access_managing.domain.ports.auth_service import (
    AuthService,
)
from taiwan_geodoc_hub.modules.access_managing.dtos.credentials import (
    Credentials,
)
from os import getenv
from uvicorn import Config, Server
from asyncio import create_task, get_running_loop, wait_for, CancelledError
from pyppeteer import launch
from pyppeteer.page import Page
from json import dumps
from contextlib import asynccontextmanager
from typing import Any, Callable, Awaitable


class AuthAdapter(AuthService):
    async def _render_sign_in_page(self, request):
        firebase_config = dumps(
            dict(
                apiKey=getenv("API_KEY"),
                authDomain=getenv("AUTH_DOMAIN"),
                projectId=getenv("PROJECT_ID"),
                storageBucket=getenv("STORAGE_BUCKET"),
                messagingSenderId=getenv("MESSAGING_SENDER_ID"),
                appId=getenv("APP_ID"),
                measurementId=getenv("MEASUREMENT_ID"),
            )
        )
        html = f"""
        <!DOCTYPE html>
            <html>
            <head>
              <title>Login</title>
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <style>
                html, body {{
                  height: 100%;
                  margin: 0;
                }}
              </style>
              <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
              <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-auth-compat.js"></script>
            </head>
            <body>
              <script type="module">
                try {{
                  firebase.initializeApp({firebase_config})
                  const {{ user }} = await firebase.auth().signInWithPopup(new firebase.auth.GoogleAuthProvider())
                  const idToken = await user.getIdToken()
                  const refreshToken = user.refreshToken
                  resolve({{ idToken, refreshToken }})
                }} catch (thrown) {{
                  reject(thrown instanceof Error ? thrown.message : String(thrown))
                }}
              </script>
            </body>
            </html>
        """
        return HTMLResponse(html.strip())

    def _create_app(self):
        app = Starlette(
            debug=False,
            routes=[
                Route("/auth/sign-in", self._render_sign_in_page),
            ],
        )
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
        return app

    @asynccontextmanager
    async def _start_server(self, port: int):
        server = Server(
            Config(
                app=self._create_app(),
                lifespan="off",
                host="0.0.0.0",
                port=port,
                log_level="error",
            )
        )
        try:
            server_task = create_task(server.serve())
            yield
        finally:
            server.should_exit = True
            try:
                server_task.cancel()
                await server_task
            except CancelledError:
                pass

    @asynccontextmanager
    async def _start_puppeteer(self):
        try:
            browser = await launch(
                headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-web-security",
                    "--disable-features=IsolateOrigins,site-per-process",
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized",
                    "--no-first-run",
                    "--no-default-browser-check",
                ],
            )
            [page] = await browser.pages()
            yield page
        finally:
            await page.close()
            await browser.close()

    async def _auth_via_puppeteer(self, page: Page, start: Callable[[], Awaitable]):
        future = get_running_loop().create_future()

        def resolve(credentials_data: dict):
            nonlocal future
            if not future.done():
                future.set_result(Credentials(**credentials_data))

        def reject(error: str):
            nonlocal future
            if not future.done():
                future.set_exception(Exception(error))

        def on_error(error: Any):
            reject(str(error))

        def on_close():
            reject("Puppeteer closed")

        page.on("error", on_error)
        page.on("close", on_close)
        await page.exposeFunction("resolve", resolve)
        await page.exposeFunction("reject", reject)
        await start()
        return await wait_for(future, timeout=300)

    async def auth(self) -> Credentials:
        port = int(getenv("AUTH_SERVICE_PORT", "3000"))

        async with self._start_server(port):
            async with self._start_puppeteer() as page:

                def start():
                    nonlocal page
                    return page.goto(f"http://localhost:{port}/auth/sign-in")

                return await self._auth_via_puppeteer(page, start)
