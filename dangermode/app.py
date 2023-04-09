import importlib.resources

from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.responses import PlainTextResponse

from dangermode.routes import router
from dangermode.suggestions import RUN_CELL_PARSE_FAIL

# We have to set the servers to show an HTTP localhost so that ChatGPT doesn't try HTTPS in development
app = FastAPI(servers=[{"url": "http://localhost:8000", "description": "Local server"}])

app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path == "/api/run_cell":
        # ChatGPT sometimes sends plaintext instead of JSON. When that
        # happens we could try to parse it as JSON. However that would
        # require us to parse the body ourselves and we would lose both the
        # type checking and OpenAPI documentation that FastAPI provides.
        #
        # We could defer to the `/api/run_cell` handler but sometimes
        # ChatGPT sends invalid JSON that looks like
        #
        # {
        #   "code": "import pandas as pd"
        #           "print('hello world')"
        # }
        #
        # Instead we'll try to hint to ChatGPT that it should send JSON
        # matching our preferred schema.
        return PlainTextResponse(RUN_CELL_PARSE_FAIL, status_code=422)

    else:
        return await request_validation_exception_handler(request, exc)


# Allow for serving the image asset from the package itself
static_directory = importlib.resources.files("dangermode") / "static"

app.mount("/static", StaticFiles(directory=str(static_directory)), name="static")


# Defined outside of the router so we can call app.openapi()
@app.get("/openapi.json", include_in_schema=False)
async def get_openapi():
    return app.openapi()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
