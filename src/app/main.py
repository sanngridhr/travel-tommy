from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.router import router
from app.database.piccolo_conf import DB


@asynccontextmanager
async def lifespan(_: FastAPI):
    await DB.start_connection_pool()

    yield

    await DB.close_connection_pool()


app: FastAPI = FastAPI(
    title="Places API",
    lifespan=lifespan,
)
app.include_router(router, prefix="/api/v1")
