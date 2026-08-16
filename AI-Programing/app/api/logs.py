from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db_session
from app.db.models import AuditLog

router = APIRouter(prefix="/logs", tags=["Audit & Execution Logs"])


@router.get("", status_code=status.HTTP_200_OK)
async def get_audit_logs(
    event_type: Optional[str] = Query(None, description="Filter by event type (TOOL_EXECUTION, HITL_REQUEST, HITL_APPROVAL)"),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db_session)
):
    """Retrieve audit trail logs recorded in PostgreSQL database."""
    stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if event_type:
        stmt = stmt.where(AuditLog.event_type == event_type)

    res = await db.execute(stmt)
    logs = res.scalars().all()

    return [
        {
            "id": log.id,
            "event_type": log.event_type,
            "action": log.action,
            "status": log.status,
            "tool_name": log.tool_name,
            "input_data": log.input_data,
            "output_data": log.output_data,
            "execution_time_ms": log.execution_time_ms,
            "created_at": log.created_at
        }
        for log in logs
    ]
