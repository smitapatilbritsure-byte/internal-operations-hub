# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
# pyrefly: ignore [missing-import]
from supabase import Client

# pyrefly: ignore [missing-import]
from core.dependencies import get_db
# pyrefly: ignore [missing-import]
from core.security import verify_password, create_access_token
# pyrefly: ignore [missing-import]
from schemas.user import Token, UserLogin
# pyrefly: ignore [missing-import]
from services.user_service import UserService

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    login_data: UserLogin, db: Client = Depends(get_db)
) -> Any:
    """
    Login to get an access token for future requests
    """
    user_service = UserService(db)
    user = user_service.get_user_by_email(email=login_data.email)
    
    if not user or not verify_password(login_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
        
    access_token = create_access_token(
        subject=user["email"],
        role=user["role"]
    )
    return {"access_token": access_token, "token_type": "bearer"}
