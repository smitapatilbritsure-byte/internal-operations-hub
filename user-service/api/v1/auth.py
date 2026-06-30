from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from supabase import Client

from core.dependencies import get_db
from core.security import verify_password, create_access_token
from schemas.user import Token
from services.user_service import UserService

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Client = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user_service = UserService(db)
    user = user_service.get_user_by_email(email=form_data.username)
    
    if not user or not verify_password(form_data.password, user["password_hash"]):
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
