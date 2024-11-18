from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from src.api.routers import router
from src.db import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # do some init setup

    yield

    if not sessionmanager.is_closed:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="test", description="test", version="1.0")
app.add_middleware(GZipMiddleware)
app.include_router(router)

@app.get("/")
@app.get("/health")
async def healthcheck():
    return {"status": "healthy"}
