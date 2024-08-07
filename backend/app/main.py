from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Iterator

import anyio
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.security.api_key import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from starlette.templating import _TemplateResponse

from app.api.router import api_router

from .settings import settings

api_description = """
## Inspect employers

## API Documentation:
- [Stoplight](https://doorlook.soulant.com/api/docs)
- [Swagger UI](https://doorlook.soulant.com/api/swagger)
- [ReDoc](https://doorlook.soulant.com/api/redoc)
"""


# @asynccontextmanager
# async def lifespan(app: FastAPI) -> Iterator[None] | AsyncGenerator[Any, Any]:
#     """
#     Context manager to set the default thread limiter for the application.
#     """
#     limiter = anyio.to_thread.current_default_thread_limiter()
#     limiter.total_tokens = 100
#     yield


app = FastAPI(
    title="Doorlook API",
    description=api_description,
    version="0.1.0",
    contact={
        "name": "Doorlook API",
        "url": "https://github.com/Gogeloo",
    },
    docs_url="/api/swagger",
    redoc_url="/api/redoc",
    # lifespan=lifespan,
)


app.add_middleware(GZipMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
# templates = Jinja2Templates(directory="app/frontend/templates")


@app.on_event("startup")
async def startup_event() -> None:
    """Startup event for the application."""
    pass


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shutdown event for the application."""
    pass


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException) -> _TemplateResponse | JSONResponse:
#     if exc.status_code == 404 and not request.url.path.startswith("/api"):
#         return templates.TemplateResponse("404.html", {"request": request})
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": str(exc.detail)},
#     )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")


# Serve the sitemap
@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse("app/static/sitemap.xml")


# Serve the robots.txt
@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse("app/static/robots.txt")


@app.get("/api/openapi.json", tags=["Documentation Formats"], include_in_schema=False)
async def get_openapi() -> JSONResponse:
    return JSONResponse(app.openapi())


@app.get("/api", include_in_schema=False)
async def api_root() -> RedirectResponse:
    return RedirectResponse(url="/api/docs")


@app.get("/", include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse(url="/api/docs")


@app.get(
    "/api/docs",
    tags=["Documentation Formats"],
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def stoplight() -> HTMLResponse:
    """
    Renders an HTML page with a stoplight using the Stoplight Elements library.
    """
    return HTMLResponse(
        """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <style>
            html,
            body {
              height: 100%;
            }
          </style>
        <title>Efficiency-6 API</title>

        <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
        <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
      </head>
      <body>

        <elements-api
          apiDescriptionUrl="openapi.json"
          router="hash"
        />

      </body>
    </html>"""
    )



app.include_router(api_router, prefix="/api/v1")


if __name__ == "__main__":
    pass
