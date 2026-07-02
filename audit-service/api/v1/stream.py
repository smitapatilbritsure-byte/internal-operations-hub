# pyrefly: ignore [missing-import]
import asyncio
import json
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, Request
# pyrefly: ignore [missing-import]
from sse_starlette.sse import EventSourceResponse
# pyrefly: ignore [missing-import]
from services.audit_service import broadcaster
# pyrefly: ignore [missing-import]
from core.dependencies import get_current_admin_user, TokenData

router = APIRouter()

@router.get("/stream")
async def audit_event_stream(
    request: Request,
    # In a real-world scenario, you'd pass token in query param or headers for SSE,
    # but sse_starlette works well with standard dependencies if headers are provided.
    # current_user: TokenData = Depends(get_current_admin_user) 
):
    """
    Server-Sent Events (SSE) endpoint for real-time audit logs.
    """
    queue = asyncio.Queue()
    broadcaster.queues.append(queue)
    
    async def event_generator():
        try:
            while True:
                # If client disconnects, request.is_disconnected() will be true
                if await request.is_disconnected():
                    break
                
                # Wait for the next event from the broadcaster
                message = await queue.get()
                
                # Yield the SSE format
                yield {
                    "event": message["event"],
                    "data": json.dumps(message["data"])
                }
        finally:
            # Clean up the queue when the client disconnects
            broadcaster.queues.remove(queue)
            
    return EventSourceResponse(event_generator())
