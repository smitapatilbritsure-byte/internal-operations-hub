from supabase import Client
from schemas.user import UserCreate, UserUpdate, UserRoleUpdate
from core.security import get_password_hash
from fastapi import HTTPException, status
import uuid

class UserService:
    def __init__(self, db: Client):
        self.db = db

    def get_user_by_id(self, user_id: str):
        response = self.db.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        return response.data[0]

    def get_user_by_email(self, email: str):
        response = self.db.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None

    def get_all_users(self, skip: int = 0, limit: int = 100):
        response = self.db.table("users").select("*").range(skip, skip + limit - 1).execute()
        return response.data

    def create_user(self, user: UserCreate):
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(user.password)
        
        new_user = {
            "full_name": user.full_name,
            "email": user.email,
            "password_hash": hashed_password,
            "role": "standard", # Default role
            "is_active": True
        }
        
        response = self.db.table("users").insert(new_user).execute()
        return response.data[0]

    def update_user(self, user_id: str, user_update: UserUpdate):
        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            return self.get_user_by_id(user_id)
            
        response = self.db.table("users").update(update_data).eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        return response.data[0]

    def update_user_role(self, user_id: str, role_update: UserRoleUpdate):
        response = self.db.table("users").update({"role": role_update.role.value}).eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        return response.data[0]

    def deactivate_user(self, user_id: str):
        response = self.db.table("users").update({"is_active": False}).eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        return response.data[0]
