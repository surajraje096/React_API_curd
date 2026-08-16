from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db_session
from app.agent.state import ChatRequest, ChatResponse
from app.agent.agent import AIAgent

router = APIRouter(prefix="/chat", tags=["Chat & Agent"])


@router.post("", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_agent(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db_session)
):
    """
    Send a natural language prompt to the AI Agent.
    - Safe function tools (reading account info, system health) are executed automatically.
    - Risky function tools (transferring money, suspending accounts) pause and return status `PENDING_APPROVAL` with an approval request ID.
    """
    try:
        agent = AIAgent(session=db)
        response = await agent.process_chat(
            user_prompt=payload.message,
            conversation_id=payload.conversation_id
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing agent chat request: {str(e)}"
        )
