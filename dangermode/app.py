from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from dangermode.routes import router

# We have to set the servers to show an HTTP localhost so that ChatGPT doesn't try HTTPS in development
app = FastAPI(servers=[{"url": "http://localhost:8000", "description": "Local server"}])

app.include_router(router)

app.mount("/static", StaticFiles(directory="dangermode/static"), name="static")


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
