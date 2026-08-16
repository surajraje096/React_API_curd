import logging
import time
import json
from typing import Dict, Any, Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Conversation, Message
from app.agent.tools import TOOL_REGISTRY, get_openai_tool_definitions
from app.agent.state import ChatResponse
from app.hitl.approval_manager import ApprovalManager
from app.logging_eval.logger import log_audit_event
from app.logging_eval.evaluator import evaluate_agent_interaction

logger = logging.getLogger(__name__)


class AIAgent:
    """Core AI Agent handling LLM reasoning, safe tool execution, and HITL risky tool interception."""

    SYSTEM_PROMPT = (
        "You are an intelligent Assistant with access to application database tools and diagnostic tools. "
        "Available tools:\n"
        "1. search_user_account: Read-only query for account info and balances.\n"
        "2. get_system_health: System metrics check.\n"
        "3. transfer_funds: Wire transfer funds between accounts (RISKY: Requires human approval).\n"
        "4. reset_user_status: Suspend or reactivate user account (RISKY: Requires human approval).\n\n"
        "Always use the appropriate tool when asked to query or modify data."
    )

    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_or_create_conversation(self, conversation_id: Optional[str]) -> Conversation:
        if conversation_id:
            stmt = select(Conversation).where(Conversation.id == conversation_id)
            res = await self.session.execute(stmt)
            conv = res.scalars().first()
            if conv:
                return conv

        # Create new conversation
        conv = Conversation(title="Chat Session")
        self.session.add(conv)
        await self.session.commit()
        await self.session.refresh(conv)
        return conv

    async def _infer_tool_call(self, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Determines tool call using OpenAI API or fallback intent parser if API key is absent."""
        if settings.OPENAI_API_KEY:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                messages = [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ]
                response = await client.chat.completions.create(
                    model=settings.DEFAULT_MODEL,
                    messages=messages,
                    tools=get_openai_tool_definitions(),
                    tool_choice="auto"
                )
                choice = response.choices[0].message
                if choice.tool_calls:
                    tool_call = choice.tool_calls[0]
                    return {
                        "name": tool_call.function.name,
                        "args": json.loads(tool_call.function.arguments),
                        "id": tool_call.id
                    }
            except Exception as e:
                logger.warning(f"OpenAI call failed or key invalid ({e}). Falling back to internal intent router.")

        # Fallback Intent Router for standalone local operation
        prompt_lower = user_prompt.lower()

        if "transfer" in prompt_lower or "send money" in prompt_lower or "pay" in prompt_lower:
            # Extract numbers/words simple parser
            import re
            numbers = re.findall(r'\$?(\d+(?:\.\d+)?)', user_prompt)
            amount = float(numbers[0]) if numbers else 100.0
            
            accounts = re.findall(r'ACC-\d+|usr-\d+|\buser \d+\b|\b\d{4}\b', user_prompt, re.IGNORECASE)
            source = accounts[0] if len(accounts) > 0 else "ACC-1001"
            dest = accounts[1] if len(accounts) > 1 else "ACC-1002"

            return {
                "name": "transfer_funds",
                "args": {
                    "source_account": source,
                    "destination_account": dest,
                    "amount": amount
                },
                "id": "call_mock_transfer"
            }

        elif "suspend" in prompt_lower or "reset" in prompt_lower or "deactivate" in prompt_lower or "activate" in prompt_lower:
            status = "suspended" if ("suspend" in prompt_lower or "deactivate" in prompt_lower) else "active"
            import re
            accounts = re.findall(r'ACC-\d+|usr-\d+|\b\d{4}\b', user_prompt, re.IGNORECASE)
            account = accounts[0] if accounts else "ACC-1001"

            return {
                "name": "reset_user_status",
                "args": {
                    "account_number": account,
                    "new_status": status,
                    "reason": "Requested via user chat prompt"
                },
                "id": "call_mock_reset"
            }

        elif "health" in prompt_lower or "status" in prompt_lower or "system" in prompt_lower or "metrics" in prompt_lower:
            return {
                "name": "get_system_health",
                "args": {},
                "id": "call_mock_health"
            }

        elif "search" in prompt_lower or "balance" in prompt_lower or "account" in prompt_lower or "user" in prompt_lower:
            import re
            queries = re.findall(r'ACC-\d+|usr-\d+|alice|bob|charlie|\b\d{4}\b', user_prompt, re.IGNORECASE)
            query = queries[0] if queries else "Alice"
            return {
                "name": "search_user_account",
                "args": {"query": query},
                "id": "call_mock_search"
            }

        return None

    async def process_chat(self, user_prompt: str, conversation_id: Optional[str] = None) -> ChatResponse:
        """Main agent turn pipeline."""
        start_time = time.time()
        conv = await self._get_or_create_conversation(conversation_id)

        # Store user message
        user_msg = Message(conversation_id=conv.id, role="user", content=user_prompt)
        self.session.add(user_msg)
        await self.session.commit()

        # Step 1: Infer tool selection
        tool_call = await self._infer_tool_call(user_prompt)

        # If no tool needed -> Direct conversational response
        if not tool_call:
            response_text = f"I have processed your request: '{user_prompt}'. No external tool call was required."
            assistant_msg = Message(conversation_id=conv.id, role="assistant", content=response_text)
            self.session.add(assistant_msg)
            await self.session.commit()

            exec_time = round((time.time() - start_time) * 1000, 2)
            await log_audit_event(
                session=self.session,
                event_type="AGENT_CHAT",
                action="Direct conversation response",
                status="SUCCESS",
                execution_time_ms=exec_time
            )

            await evaluate_agent_interaction(
                session=self.session,
                user_prompt=user_prompt,
                agent_response=response_text,
                expected_tool=None,
                actual_tool=None,
                conversation_id=conv.id
            )

            return ChatResponse(
                conversation_id=conv.id,
                response=response_text,
                status="COMPLETED",
                approval_required=False
            )

        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_meta = TOOL_REGISTRY.get(tool_name)

        if not tool_meta:
            error_text = f"Tool '{tool_name}' is not registered."
            return ChatResponse(conversation_id=conv.id, response=error_text, status="FAILED")

        # Step 2: Check if tool is RISKY and requires Human Approval
        if tool_meta.get("is_risky", False):
            logger.info(f"INTERCEPTED RISKY TOOL: {tool_name}. Halting execution & creating approval request.")
            
            approval = await ApprovalManager.create_pending_approval(
                session=self.session,
                conversation_id=conv.id,
                tool_name=tool_name,
                tool_args=tool_args,
                risk_level=tool_meta.get("risk_level", "HIGH"),
                justification=f"Action '{tool_name}' modifies user data or financial balances."
            )

            response_text = (
                f"Action '{tool_name}' involves a sensitive/risky action. "
                f"Execution has been paused and submitted for Human Approval (Approval ID: {approval.id})."
            )

            assistant_msg = Message(
                conversation_id=conv.id,
                role="assistant",
                content=response_text,
                tool_calls={"tool_name": tool_name, "tool_args": tool_args, "approval_id": approval.id}
            )
            self.session.add(assistant_msg)
            await self.session.commit()

            await evaluate_agent_interaction(
                session=self.session,
                user_prompt=user_prompt,
                agent_response=response_text,
                expected_tool=tool_name,
                actual_tool=tool_name,
                is_risky_tool=True,
                approval_required=True,
                conversation_id=conv.id
            )

            return ChatResponse(
                conversation_id=conv.id,
                response=response_text,
                status="PENDING_APPROVAL",
                approval_required=True,
                approval_details={
                    "approval_id": approval.id,
                    "tool_name": tool_name,
                    "tool_args": tool_args,
                    "risk_level": approval.risk_level,
                    "justification": approval.justification
                }
            )

        # Step 3: Execute SAFE tool directly
        logger.info(f"Executing safe tool: {tool_name}")
        func = tool_meta["func"]
        tool_result = await func(self.session, **tool_args)

        response_text = f"Executed {tool_name}. Result: {json.dumps(tool_result, indent=2)}"
        assistant_msg = Message(
            conversation_id=conv.id,
            role="assistant",
            content=response_text,
            tool_calls={"tool_name": tool_name, "result": tool_result}
        )
        self.session.add(assistant_msg)
        await self.session.commit()

        exec_time = round((time.time() - start_time) * 1000, 2)
        await log_audit_event(
            session=self.session,
            event_type="TOOL_EXECUTION",
            action=f"Executed safe tool {tool_name}",
            status="SUCCESS",
            tool_name=tool_name,
            input_data=tool_args,
            output_data=tool_result,
            execution_time_ms=exec_time
        )

        await evaluate_agent_interaction(
            session=self.session,
            user_prompt=user_prompt,
            agent_response=response_text,
            expected_tool=tool_name,
            actual_tool=tool_name,
            is_risky_tool=False,
            approval_required=False,
            conversation_id=conv.id
        )

        return ChatResponse(
            conversation_id=conv.id,
            response=response_text,
            status="COMPLETED",
            approval_required=False,
            tool_executed=tool_name,
            execution_result=tool_result
        )
