import sys
import os

# Ensure we can import from shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# pyrefly: ignore [missing-import]
from fastapi import Depends, HTTPException, status
# pyrefly: ignore [missing-import]
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# pyrefly: ignore [missing-import]
from jose import jwt, JWTError
# pyrefly: ignore [missing-import]
from pydantic import ValidationError
# pyrefly: ignore [missing-import]
from core.config import settings
# pyrefly: ignore [missing-import]
from schemas.user import TokenData
# pyrefly: ignore [missing-import]
from shared.supabase_client import get_supabase_client
# pyrefly: ignore [missing-import]
from supabase import Client

security = HTTPBearer()

def get_db() -> Client:
    return get_supabase_client()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TokenData:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        token_data = TokenData(email=email, role=role)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return token_data

def get_current_active_user(
    current_user: TokenData = Depends(get_current_user),
) -> TokenData:
    # Here you might want to query DB to check if user is active
    # For now, we trust the token if it's valid
    return current_user

def get_current_admin_user(
    current_user: TokenData = Depends(get_current_active_user),
) -> TokenData:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user
