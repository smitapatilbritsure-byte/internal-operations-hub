from fastapi import APIRouter, Depends, Query
from supabase import Client
from typing import List, Any
from core.dependencies import get_db, get_current_active_user, get_current_admin_user, TokenData
from schemas.request import RequestCreate, RequestResponse, RequestOverride
from services.request_service import RequestService

router = APIRouter()

@router.post("/", response_model=RequestResponse)
def create_request(
    request_in: RequestCreate,
    db: Client = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
) -> Any:
    """
    Create a new request.
    Admins: Auto-approved.
    Standard Users: Marked as pending.
    """
    service = RequestService(db)
    return service.create_request(request_in, current_user)

@router.get("/", response_model=List[RequestResponse])
def get_requests(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Client = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
) -> Any:
    """
    List requests.
    Admins: Retrieve all requests.
    Standard Users: Retrieve only their own requests.
    """
    service = RequestService(db)
    return service.get_all_requests(current_user, skip=skip, limit=limit)

@router.get("/{request_id}", response_model=RequestResponse)
def get_request(
    request_id: str,
    db: Client = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user)
) -> Any:
    """
    Get details of a specific request by ID.
    Standard Users: Access restricted to own requests.
    """
    service = RequestService(db)
    return service.get_request_by_id(request_id, current_user)

@router.post("/{request_id}/override", response_model=RequestResponse)
def override_request(
    request_id: str,
    override_in: RequestOverride,
    db: Client = Depends(get_db),
    current_admin: TokenData = Depends(get_current_admin_user)
) -> Any:
    """
    Override status of a pending request (Approve/Reject).
    Admins only.
    """
    service = RequestService(db)
    return service.override_request(request_id, override_in, current_admin)
