import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PendingApproval, AuditLog, Conversation, Message
from app.agent.tools import TOOL_REGISTRY
from app.logging_eval.logger import log_audit_event

logger = logging.getLogger(__name__)


class ApprovalManager:
    """Manages creation, retrieval, authorization, and execution of human-approved risky tools."""

    @staticmethod
    async def create_pending_approval(
        session: AsyncSession,
        conversation_id: str,
        tool_name: str,
        tool_args: Dict[str, Any],
        risk_level: str = "HIGH",
        justification: str = "Risky action requires human authorization."
    ) -> PendingApproval:
        """Record a pending approval request in PostgreSQL database."""
        approval = PendingApproval(
            conversation_id=conversation_id,
            tool_name=tool_name,
            tool_args=tool_args,
            risk_level=risk_level,
            justification=justification,
            status="PENDING"
        )
        session.add(approval)
        await session.commit()
        await session.refresh(approval)

        # Audit log creation
        await log_audit_event(
            session=session,
            event_type="HITL_REQUEST",
            action=f"Requested approval for risky tool {tool_name}",
            status="PENDING",
            tool_name=tool_name,
            input_data=tool_args,
            output_data={"approval_id": approval.id, "risk_level": risk_level}
        )

        logger.info(f"Created PendingApproval id={approval.id} for tool={tool_name}")
        return approval

    @staticmethod
    async def list_pending_approvals(session: AsyncSession) -> List[PendingApproval]:
        """Fetch all requests awaiting human approval."""
        stmt = select(PendingApproval).where(PendingApproval.status == "PENDING").order_by(PendingApproval.requested_at.desc())
        res = await session.execute(stmt)
        return list(res.scalars().all())

    @staticmethod
    async def get_approval_by_id(session: AsyncSession, approval_id: str) -> Optional[PendingApproval]:
        """Fetch a specific approval request by ID."""
        stmt = select(PendingApproval).where(PendingApproval.id == approval_id)
        res = await session.execute(stmt)
        return res.scalars().first()

    @staticmethod
    async def process_approval_response(
        session: AsyncSession,
        approval_id: str,
        action: str,
        responded_by: str = "admin@company.com",
        rejection_reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """Processes human decision (APPROVED / REJECTED) and executes tool if approved."""
        approval = await ApprovalManager.get_approval_by_id(session, approval_id)
        if not approval:
            raise ValueError(f"Approval request '{approval_id}' not found.")

        if approval.status != "PENDING":
            return {
                "success": False,
                "message": f"Approval request already has status '{approval.status}'."
            }

        approval.responded_at = datetime.utcnow()
        approval.responded_by = responded_by

        if action.upper() == "REJECTED":
            approval.status = "REJECTED"
            approval.rejection_reason = rejection_reason or "Operation rejected by administrator."
            await session.commit()

            # Record assistant message in conversation
            rejection_msg = Message(
                conversation_id=approval.conversation_id,
                role="assistant",
                content=f"[HUMAN APPROVAL DENIED] Action '{approval.tool_name}' was rejected by {responded_by}. Reason: {approval.rejection_reason}"
            )
            session.add(rejection_msg)
            await session.commit()

            await log_audit_event(
                session=session,
                event_type="HITL_APPROVAL",
                action=f"Rejected risky tool {approval.tool_name}",
                status="REJECTED",
                tool_name=approval.tool_name,
                input_data=approval.tool_args,
                output_data={"rejection_reason": approval.rejection_reason}
            )

            return {
                "success": True,
                "status": "REJECTED",
                "message": f"Action '{approval.tool_name}' rejected.",
                "execution_result": None
            }

        elif action.upper() == "APPROVED":
            approval.status = "APPROVED"
            
            # Execute tool function registered in TOOL_REGISTRY
            tool_meta = TOOL_REGISTRY.get(approval.tool_name)
            if not tool_meta:
                approval.status = "FAILED"
                await session.commit()
                return {"success": False, "message": f"Tool '{approval.tool_name}' not registered in registry."}

            try:
                func = tool_meta["func"]
                execution_result = await func(session, **approval.tool_args)
                approval.execution_result = execution_result
                await session.commit()

                # Add assistant message to conversation thread
                assistant_msg = Message(
                    conversation_id=approval.conversation_id,
                    role="assistant",
                    content=f"[HUMAN APPROVAL GRANTED] Action '{approval.tool_name}' was approved and executed successfully.\nResult: {execution_result.get('message', execution_result)}"
                )
                session.add(assistant_msg)
                await session.commit()

                await log_audit_event(
                    session=session,
                    event_type="HITL_APPROVAL",
                    action=f"Approved and executed risky tool {approval.tool_name}",
                    status="SUCCESS",
                    tool_name=approval.tool_name,
                    input_data=approval.tool_args,
                    output_data=execution_result
                )

                return {
                    "success": True,
                    "status": "APPROVED",
                    "message": f"Action '{approval.tool_name}' approved and executed.",
                    "execution_result": execution_result
                }
            except Exception as e:
                logger.error(f"Error executing approved tool {approval.tool_name}: {e}")
                approval.status = "FAILED"
                approval.execution_result = {"error": str(e)}
                await session.commit()
                return {"success": False, "message": f"Execution failed: {str(e)}"}

        else:
            raise ValueError("Invalid action. Must be 'APPROVED' or 'REJECTED'.")
