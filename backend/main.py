from fastapi import FastAPI
from api.routes import auth_router, content_router, search_router, users_router

app = FastAPI(title="video semantic search api",
 description="API for semantic search of videos", )


app.include_router(auth_router.router)
app.include_router(content_router.router)
app.include_router(search_router.router)
app.include_router(users_router.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}

