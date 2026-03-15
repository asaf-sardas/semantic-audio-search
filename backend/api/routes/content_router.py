from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/content", tags=["Content"])

@router.get("/{id}/status")
def get_status(id: str):
    return {"message": "Status retrieved successfully"}

@router.post("/process")
def process():
    return {"message": "Content processed successfully"}