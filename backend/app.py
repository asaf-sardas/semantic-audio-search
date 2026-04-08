from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.api.routes import auth_router, content_router, search_router, users_router
from backend.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="video semantic search api",
    description="API for semantic search of videos",
    lifespan=lifespan,
)

app.include_router(auth_router.router)
app.include_router(content_router.router)
app.include_router(search_router.router)
app.include_router(users_router.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
