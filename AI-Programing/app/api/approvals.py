from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db_session
from app.hitl.approval_manager import ApprovalManager
from app.agent.state import ApprovalActionRequest, ApprovalActionResponse

router = APIRouter(prefix="/approvals", tags=["Human Approvals (HITL)"])


@router.get("", status_code=status.HTTP_200_OK)
async def list_pending_approvals(db: AsyncSession = Depends(get_db_session)):
    """List all risky tool execution requests currently waiting for human approval."""
    approvals = await ApprovalManager.list_pending_approvals(db)
    return [
        {
            "id": app.id,
            "conversation_id": app.conversation_id,
            "tool_name": app.tool_name,
            "tool_args": app.tool_args,
            "risk_level": app.risk_level,
            "justification": app.justification,
            "status": app.status,
            "requested_at": app.requested_at
        }
        for app in approvals
    ]


@router.get("/{approval_id}", status_code=status.HTTP_200_OK)
async def get_approval_details(
    approval_id: str,
    db: AsyncSession = Depends(get_db_session)
):
    """Retrieve details for a specific approval request."""
    app = await ApprovalManager.get_approval_by_id(db, approval_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Approval request '{approval_id}' not found.")
    return {
        "id": app.id,
        "conversation_id": app.conversation_id,
        "tool_name": app.tool_name,
        "tool_args": app.tool_args,
        "risk_level": app.risk_level,
        "justification": app.justification,
        "status": app.status,
        "requested_at": app.requested_at,
        "responded_at": app.responded_at,
        "responded_by": app.responded_by,
        "rejection_reason": app.rejection_reason,
        "execution_result": app.execution_result
    }


@router.post("/{approval_id}/respond", response_model=ApprovalActionResponse, status_code=status.HTTP_200_OK)
async def respond_to_approval(
    approval_id: str,
    payload: ApprovalActionRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Human Authorization Endpoint:
    - Set action to `APPROVED` to authorize execution of the risky function tool.
    - Set action to `REJECTED` to deny execution of the risky tool.
    """
    try:
        result = await ApprovalManager.process_approval_response(
            session=db,
            approval_id=approval_id,
            action=payload.action,
            responded_by=payload.responded_by,
            rejection_reason=payload.rejection_reason
        )
        return ApprovalActionResponse(
            approval_id=approval_id,
            status=result.get("status", payload.action.upper()),
            message=result.get("message", "Processed decision successfully."),
            execution_result=result.get("execution_result")
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process approval response: {str(e)}"
        )
