import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, Text, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserAccount(Base):
    """Application domain user model."""
    __tablename__ = "user_accounts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    balance: Mapped[float] = mapped_column(Float, default=1000.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Conversation(Base):
    """Conversation thread tracking agent interactions."""
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200), default="New Chat")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    pending_approvals: Mapped[list["PendingApproval"]] = relationship("PendingApproval", back_populates="conversation")


class Message(Base):
    """Individual messages within a conversation thread."""
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[str] = mapped_column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(20)) # system, user, assistant, tool
    content: Mapped[str] = mapped_column(Text, default="")
    tool_calls: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    tool_call_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")


class PendingApproval(Base):
    """Tracks risky function tool actions awaiting human authorization."""
    __tablename__ = "pending_approvals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[str] = mapped_column(String(36), ForeignKey("conversations.id"), index=True)
    tool_name: Mapped[str] = mapped_column(String(100))
    tool_args: Mapped[Dict[str, Any]] = mapped_column(JSON)
    justification: Mapped[str] = mapped_column(Text)
    risk_level: Mapped[str] = mapped_column(String(20), default="HIGH") # LOW, MEDIUM, HIGH, CRITICAL
    status: Mapped[str] = mapped_column(String(20), default="PENDING") # PENDING, APPROVED, REJECTED
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    responded_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    responded_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    execution_result: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="pending_approvals")


class AuditLog(Base):
    """Structured audit logs for agent actions, tool calls, and human approvals."""
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    event_type: Mapped[str] = mapped_column(String(50), index=True) # TOOL_CALL, HITL_REQUEST, HITL_APPROVAL, SYSTEM_EVENT
    action: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20)) # SUCCESS, PENDING, REJECTED, FAILED
    tool_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    input_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    output_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    execution_time_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class EvaluationRun(Base):
    """Evaluation runs measuring agent response quality, safety, and correctness."""
    __tablename__ = "evaluation_runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    user_prompt: Mapped[str] = mapped_column(Text)
    agent_response: Mapped[str] = mapped_column(Text)
    expected_tool: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    actual_tool: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    tool_selection_accuracy: Mapped[float] = mapped_column(Float, default=1.0) # 0.0 to 1.0
    faithfulness_score: Mapped[float] = mapped_column(Float, default=1.0) # 0.0 to 1.0
    safety_score: Mapped[float] = mapped_column(Float, default=1.0) # 1.0 if risky action correctly flagged HITL
    overall_score: Mapped[float] = mapped_column(Float, default=1.0)
    feedback: Mapped[str] = mapped_column(Text, default="Automated evaluation passed.")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
