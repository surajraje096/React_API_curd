from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AgentMessage(BaseModel):
    role: str # user, assistant, system, tool
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_call_id: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = Field(..., description="User prompt to the agent")
    conversation_id: Optional[str] = Field(None, description="Existing conversation thread ID")


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    status: str = Field("COMPLETED", description="COMPLETED, PENDING_APPROVAL, or REJECTED")
    approval_required: bool = False
    approval_details: Optional[Dict[str, Any]] = None
    tool_executed: Optional[str] = None
    execution_result: Optional[Dict[str, Any]] = None


class ApprovalActionRequest(BaseModel):
    action: str = Field(..., description="APPROVED or REJECTED")
    responded_by: str = Field("admin@company.com", description="User ID or email of approver")
    rejection_reason: Optional[str] = Field(None, description="Reason if action is REJECTED")


class ApprovalActionResponse(BaseModel):
    approval_id: str
    status: str # APPROVED, REJECTED
    message: str
    execution_result: Optional[Dict[str, Any]] = None
