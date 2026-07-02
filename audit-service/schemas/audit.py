# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime

class AuditEventCreate(BaseModel):
    service_name: str = Field(..., description="Name of the service originating the event")
    event_type: str = Field(..., description="Type of event, e.g., USER_CREATED, REQUEST_APPROVED")
    actor_id: Optional[str] = Field(None, description="ID of the user performing the action")
    resource_id: Optional[str] = Field(None, description="ID of the resource affected")
    payload: Optional[Dict[str, Any]] = Field(None, description="Detailed event data")

class AuditEventResponse(AuditEventCreate):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class AuditEventList(BaseModel):
    total: int
    items: list[AuditEventResponse]
