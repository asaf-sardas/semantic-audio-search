from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register")
def register():
    return {"message": "User registered successfully"}

@router.post("/login")
def login():
    return {"message": "User logged in successfully"}