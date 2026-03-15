from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/search", tags=["Search"])

@router.post("/")
def search(query: str):
    return {"message": "Search successful"}