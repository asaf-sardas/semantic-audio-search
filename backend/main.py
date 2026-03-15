from fastapi import FastAPI

app = FastAPI(title="video semantic search api",
 description="API for semantic search of videos", )

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/api/v1/content/{id}/status")
def get_status(id: str):
    return {"content_id": id, "status": "pending"}