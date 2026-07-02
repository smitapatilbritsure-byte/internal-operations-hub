# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Any, List, Optional
# pyrefly: ignore [missing-import]
from supabase import Client
# pyrefly: ignore [missing-import]
from schemas.audit import AuditEventCreate, AuditEventResponse, AuditEventList
# pyrefly: ignore [missing-import]
from core.dependencies import get_db, get_current_admin_user, get_current_user, TokenData
# pyrefly: ignore [missing-import]
from services.audit_service import AuditService

router = APIRouter()

def get_audit_service(db: Client = Depends(get_db)) -> AuditService:
    return AuditService(db)

@router.post("/events", response_model=AuditEventResponse, status_code=status.HTTP_201_CREATED)
async def create_audit_event(
    event: AuditEventCreate,
    service: AuditService = Depends(get_audit_service)
    # Note: Depending on internal security, this endpoint might be protected by an API Key instead of a user JWT,
    # because other microservices will call it. For now, it's open or we assume microservices have a way to call it.
) -> Any:
    """
    Webhook to receive audit events from other microservices.
    """
    try:
        return await service.create_event(event)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create audit event: {str(e)}"
        )

@router.get("", response_model=AuditEventList)
def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service_name: Optional[str] = None,
    event_type: Optional[str] = None,
    service: AuditService = Depends(get_audit_service),
    current_user: TokenData = Depends(get_current_admin_user)
) -> Any:
    """
    Get audit logs with pagination and filtering. Only accessible by admins.
    """
    try:
        return service.get_events(skip, limit, service_name, event_type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch audit logs: {str(e)}"
        )

@router.get("/recent", response_model=List[AuditEventResponse])
def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    service: AuditService = Depends(get_audit_service),
    current_user: TokenData = Depends(get_current_admin_user)
) -> Any:
    """
    Get recent audit logs. Only accessible by admins.
    """
    try:
        return service.get_recent_activity(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch recent activity: {str(e)}"
        )

@router.get("/{log_id}", response_model=AuditEventResponse)
def get_audit_log_by_id(
    log_id: str,
    service: AuditService = Depends(get_audit_service),
    current_user: TokenData = Depends(get_current_admin_user)
) -> Any:
    """
    Get a specific audit log by ID. Only accessible by admins.
    """
    try:
        log = service.get_event_by_id(log_id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audit log not found"
            )
        return log
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch audit log: {str(e)}"
        )
