from typing import Any, List
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from supabase import Client

# pyrefly: ignore [missing-import]
from schemas.user import UserCreate, UserUpdate, UserResponse, UserRoleUpdate, TokenData
# pyrefly: ignore [missing-import]
from core.dependencies import get_db, get_current_user, get_current_admin_user
# pyrefly: ignore [missing-import]
from services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Client = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user_service = UserService(db)
    user = user_service.create_user(user_in)
    return user

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Client = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
) -> Any:
    """
    Retrieve users.
    """
    user_service = UserService(db)
    users = user_service.get_all_users(skip=skip, limit=limit)
    return users

@router.get("/me", response_model=UserResponse)
def read_user_me(
    db: Client = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_email(email=current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Client = Depends(get_db),
    user_in: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
) -> Any:
    """
    Update own user profile.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_email(email=current_user.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user = user_service.update_user(user_id=user["id"], user_update=user_in)
    return user

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: str,
    db: Client = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
) -> Any:
    """
    Get a specific user by id.
    """
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id=user_id)
    return user

@router.put("/{user_id}/role", response_model=UserResponse)
def update_user_role(
    *,
    db: Client = Depends(get_db),
    user_id: str,
    role_in: UserRoleUpdate,
    current_user: TokenData = Depends(get_current_admin_user),
) -> Any:
    """
    Update a user's role (Admin only).
    """
    user_service = UserService(db)
    user = user_service.update_user_role(user_id=user_id, role_update=role_in)
    return user

@router.delete("/{user_id}", response_model=UserResponse)
def deactivate_user(
    *,
    db: Client = Depends(get_db),
    user_id: str,
    current_user: TokenData = Depends(get_current_admin_user),
) -> Any:
    """
    Deactivate a user (Admin only).
    """
    user_service = UserService(db)
    user = user_service.deactivate_user(user_id=user_id)
    return user
