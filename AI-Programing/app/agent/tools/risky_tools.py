import logging
from typing import Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserAccount
from app.agent.tools import register_tool

logger = logging.getLogger(__name__)


@register_tool(
    name="transfer_funds",
    description="Transfer money from a sender account to a recipient account. RISKY ACTION: Requires Human Approval.",
    parameters={
        "type": "object",
        "properties": {
            "source_account": {
                "type": "string",
                "description": "Account number or ID of the sender"
            },
            "destination_account": {
                "type": "string",
                "description": "Account number or ID of the recipient"
            },
            "amount": {
                "type": "number",
                "description": "Amount to transfer in USD"
            }
        },
        "required": ["source_account", "destination_account", "amount"]
    },
    is_risky=True,
    risk_level="HIGH"
)
async def transfer_funds(
    session: AsyncSession,
    source_account: str,
    destination_account: str,
    amount: float
) -> Dict[str, Any]:
    """Executes money transfer after human approval has been granted."""
    logger.info(f"Executing approved risky tool transfer_funds: {amount} from {source_account} to {destination_account}")
    
    if amount <= 0:
        return {"success": False, "error": "Transfer amount must be greater than zero."}

    # Fetch source user
    sender_stmt = select(UserAccount).where(
        (UserAccount.account_number == source_account) | (UserAccount.id == source_account)
    )
    sender_res = await session.execute(sender_stmt)
    sender = sender_res.scalars().first()

    # Fetch recipient user
    recip_stmt = select(UserAccount).where(
        (UserAccount.account_number == destination_account) | (UserAccount.id == destination_account)
    )
    recip_res = await session.execute(recip_stmt)
    recipient = recip_res.scalars().first()

    if not sender:
        return {"success": False, "error": f"Sender account '{source_account}' not found."}
    if not recipient:
        return {"success": False, "error": f"Recipient account '{destination_account}' not found."}
    if sender.balance < amount:
        return {
            "success": False,
            "error": f"Insufficient funds. Sender balance is ${sender.balance:.2f}, transfer requested ${amount:.2f}."
        }

    # Perform balance transfer
    sender.balance -= amount
    recipient.balance += amount
    await session.commit()

    return {
        "success": True,
        "message": f"Successfully transferred ${amount:.2f} from {sender.full_name} to {recipient.full_name}.",
        "sender_new_balance": sender.balance,
        "recipient_new_balance": recipient.balance
    }


@register_tool(
    name="reset_user_status",
    description="Suspend, activate, or reset user account status and access permissions. CRITICAL RISKY ACTION.",
    parameters={
        "type": "object",
        "properties": {
            "account_number": {
                "type": "string",
                "description": "Account number or ID of the user"
            },
            "new_status": {
                "type": "string",
                "enum": ["active", "suspended"],
                "description": "New account status"
            },
            "reason": {
                "type": "string",
                "description": "Administrative reason for status change"
            }
        },
        "required": ["account_number", "new_status", "reason"]
    },
    is_risky=True,
    risk_level="CRITICAL"
)
async def reset_user_status(
    session: AsyncSession,
    account_number: str,
    new_status: str,
    reason: str
) -> Dict[str, Any]:
    """Executes account status reset after human approval."""
    logger.info(f"Executing approved risky tool reset_user_status: account={account_number}, new_status={new_status}")
    
    stmt = select(UserAccount).where(
        (UserAccount.account_number == account_number) | (UserAccount.id == account_number)
    )
    res = await session.execute(stmt)
    user = res.scalars().first()

    if not user:
        return {"success": False, "error": f"Account '{account_number}' not found."}

    user.is_active = (new_status.lower() == "active")
    await session.commit()

    return {
        "success": True,
        "message": f"Account {user.account_number} ({user.full_name}) status updated to {new_status.upper()}.",
        "is_active": user.is_active,
        "reason": reason
    }
