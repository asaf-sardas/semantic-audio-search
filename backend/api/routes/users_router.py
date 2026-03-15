from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/users", tags=["Users and History"])

@router.put("/profile")
def update_profile():
    return {"message": "Profile updated successfully"}

@router.get("/history")
def get_history():
        return {"message": "History retrieved successfully"}

@router.delete("/history/{id}")
def delete_history_item(id: str):
    return {"message": "History item deleted successfully"}

@router.delete("/history")
def clear_all_history():
    return {"message": "All search history cleared"}