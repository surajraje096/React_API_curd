import logging
import json
from typing import Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AuditLog

# Standard Python logger
logger = logging.getLogger("agent.audit")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


async def log_audit_event(
    session: AsyncSession,
    event_type: str,
    action: str,
    status: str,
    tool_name: Optional[str] = None,
    input_data: Optional[Dict[str, Any]] = None,
    output_data: Optional[Dict[str, Any]] = None,
    execution_time_ms: Optional[float] = None
) -> AuditLog:
    """Log structured execution audit event to PostgreSQL audit_logs table."""
    audit_entry = AuditLog(
        event_type=event_type,
        action=action,
        status=status,
        tool_name=tool_name,
        input_data=input_data,
        output_data=output_data,
        execution_time_ms=execution_time_ms
    )
    session.add(audit_entry)
    await session.commit()
    await session.refresh(audit_entry)

    # Console JSON structured log
    log_payload = {
        "event": "AUDIT_LOG",
        "id": audit_entry.id,
        "type": event_type,
        "action": action,
        "status": status,
        "tool": tool_name,
        "execution_ms": execution_time_ms
    }
    logger.info(json.dumps(log_payload))

    return audit_entry
