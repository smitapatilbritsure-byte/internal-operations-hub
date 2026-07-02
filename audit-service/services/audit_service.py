# pyrefly: ignore [missing-import]
import asyncio
import json
from typing import Optional, List, Dict, Any
# pyrefly: ignore [missing-import]
from supabase import Client
# pyrefly: ignore [missing-import]
from schemas.audit import AuditEventCreate, AuditEventResponse

class EventBroadcaster:
    def __init__(self):
        self.queues: List[asyncio.Queue] = []

    async def broadcast(self, message: Dict[str, Any]):
        for queue in self.queues:
            await queue.put(message)

broadcaster = EventBroadcaster()

class AuditService:
    def __init__(self, db: Client):
        self.db = db

    async def create_event(self, event: AuditEventCreate) -> AuditEventResponse:
        # Insert into Supabase
        data = event.model_dump()
        result = self.db.table("audit_logs").insert(data).execute()
        
        if not result.data:
            raise Exception("Failed to insert audit log")
            
        created_event = result.data[0]
        
        # Broadcast to connected SSE clients
        await broadcaster.broadcast({
            "event": "new_audit_log",
            "data": created_event
        })
        
        return AuditEventResponse(**created_event)

    def get_events(
        self, 
        skip: int = 0, 
        limit: int = 50, 
        service_name: Optional[str] = None, 
        event_type: Optional[str] = None
    ) -> Dict[str, Any]:
        
        query = self.db.table("audit_logs").select("*", count="exact")
        
        if service_name:
            query = query.eq("service_name", service_name)
        if event_type:
            query = query.eq("event_type", event_type)
            
        query = query.order("created_at", desc=True)
        query = query.range(skip, skip + limit - 1)
        
        result = query.execute()
        
        return {
            "total": result.count if result.count is not None else 0,
            "items": [AuditEventResponse(**item) for item in result.data]
        }

    def get_event_by_id(self, log_id: str) -> Optional[AuditEventResponse]:
        result = self.db.table("audit_logs").select("*").eq("id", log_id).execute()
        if not result.data:
            return None
        return AuditEventResponse(**result.data[0])
        
    def get_recent_activity(self, limit: int = 10) -> List[AuditEventResponse]:
        result = self.db.table("audit_logs").select("*").order("created_at", desc=True).limit(limit).execute()
        return [AuditEventResponse(**item) for item in result.data]
