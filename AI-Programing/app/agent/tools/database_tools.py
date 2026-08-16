import logging
from typing import Dict, Any, Optional
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserAccount
from app.agent.tools import register_tool

logger = logging.getLogger(__name__)


@register_tool(
    name="search_user_account",
    description="Search for user account details by account number, email, or user ID. Read-only operation.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Account number, email, or user ID to query"
            }
        },
        "required": ["query"]
    },
    is_risky=False,
    risk_level="LOW"
)
async def search_user_account(session: AsyncSession, query: str) -> Dict[str, Any]:
    """Execute search for a user account."""
    logger.info(f"Executing safe tool search_user_account with query='{query}'")
    stmt = select(UserAccount).where(
        or_(
            UserAccount.account_number == query,
            UserAccount.email == query,
            UserAccount.id == query,
            UserAccount.full_name.ilike(f"%{query}%")
        )
    )
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        return {
            "found": False,
            "message": f"No account found matching query '{query}'."
        }

    return {
        "found": True,
        "user": {
            "id": user.id,
            "account_number": user.account_number,
            "full_name": user.full_name,
            "email": user.email,
            "balance": user.balance,
            "is_active": user.is_active
        }
    }


@register_tool(
    name="get_system_health",
    description="Fetch system diagnostic metrics, database connectivity, and active services status.",
    parameters={
        "type": "object",
        "properties": {},
        "required": []
    },
    is_risky=False,
    risk_level="LOW"
)
async def get_system_health(session: AsyncSession) -> Dict[str, Any]:
    """Execute system health check."""
    logger.info("Executing safe tool get_system_health")
    try:
        # Simple DB ping
        await session.execute(select(1))
        db_status = "HEALTHY"
    except Exception as e:
        db_status = f"UNHEALTHY: {str(e)}"

    return {
        "system_status": "OPERATIONAL",
        "database_status": db_status,
        "services": {
            "fastapi_api": "RUNNING",
            "agent_orchestrator": "ACTIVE",
            "approval_manager": "LISTENING"
        }
    }
