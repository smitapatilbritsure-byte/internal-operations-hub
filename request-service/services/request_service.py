from supabase import Client
from fastapi import HTTPException, status
from schemas.request import RequestCreate, RequestOverride, RequestStatus
from typing import Dict, Any, List

class RequestService:
    def __init__(self, db: Client):
        self.db = db

    def create_request(self, request_in: RequestCreate, user: Dict[str, Any]) -> Dict[str, Any]:
        user_role = user.get("role")
        user_id = user.get("id")
        
        # Logic gate: Auto-approve requests created by admins
        if user_role == "admin":
            status_val = RequestStatus.approved.value
            auto_approved = True
        else:
            status_val = RequestStatus.pending.value
            auto_approved = False

        new_request = {
            "user_id": str(user_id),
            "request_type": request_in.request_type.value,
            "title": request_in.title,
            "description": request_in.description,
            "status": status_val,
            "auto_approved": auto_approved,
            "metadata": request_in.metadata
        }

        response = self.db.table("requests").insert(new_request).execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create request in database"
            )
        return response.data[0]

    def get_request_by_id(self, request_id: str, user: Dict[str, Any]) -> Dict[str, Any]:
        response = self.db.table("requests").select("*").eq("id", request_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found"
            )
        
        req = response.data[0]
        # Standard users can only view their own requests
        if user.get("role") != "admin" and req.get("user_id") != str(user.get("id")):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this request"
            )
        return req

    def get_all_requests(self, user: Dict[str, Any], skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        query = self.db.table("requests").select("*")
        
        # Standard users see only their own requests
        if user.get("role") != "admin":
            query = query.eq("user_id", str(user.get("id")))
            
        response = query.range(skip, skip + limit - 1).execute()
        return response.data

    def override_request(self, request_id: str, override_in: RequestOverride, admin_user: Dict[str, Any]) -> Dict[str, Any]:
        # Get existing request
        response = self.db.table("requests").select("*").eq("id", request_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found"
            )
            
        req = response.data[0]
        if req.get("status") != RequestStatus.pending.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending requests can be overridden"
            )

        # Update request status
        update_data = {
            "status": override_in.status.value,
            "override_by": str(admin_user.get("id")),
            "override_reason": override_in.override_reason
        }

        update_response = self.db.table("requests").update(update_data).eq("id", request_id).execute()
        if not update_response.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update request override status"
            )
        return update_response.data[0]
