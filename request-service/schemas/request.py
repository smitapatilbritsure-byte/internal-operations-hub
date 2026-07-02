from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime
from enum import Enum
import uuid

class RequestType(str, Enum):
    shift_change = "shift_change"
    tool_access = "tool_access"
    other = "other"

class RequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class RequestBase(BaseModel):
    request_type: RequestType
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class RequestCreate(RequestBase):
    pass

class RequestOverride(BaseModel):
    status: RequestStatus # Typically approved or rejected
    override_reason: str = Field(..., min_length=1)

class RequestResponse(RequestBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: RequestStatus
    auto_approved: bool
    override_by: Optional[uuid.UUID] = None
    override_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
