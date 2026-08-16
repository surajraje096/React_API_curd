import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.db.base import Base
from app.db.models import UserAccount, PendingApproval, AuditLog, EvaluationRun
from app.hitl.approval_manager import ApprovalManager
from app.agent.agent import AIAgent

# Test SQLite in-memory database
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_db_session():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed initial test data
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        user1 = UserAccount(
            id="usr-1", account_number="ACC-1001", full_name="Alice Test", email="alice@test.com", balance=1000.0, is_active=True
        )
        user2 = UserAccount(
            id="usr-2", account_number="ACC-1002", full_name="Bob Test", email="bob@test.com", balance=500.0, is_active=True
        )
        session.add_all([user1, user2])
        await session.commit()

        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_safe_tool_execution(test_db_session: AsyncSession):
    """Test that a safe tool (search_user_account) executes directly without approval."""
    agent = AIAgent(session=test_db_session)
    response = await agent.process_chat(user_prompt="Search user account for Alice")

    assert response.status == "COMPLETED"
    assert response.approval_required is False
    assert response.tool_executed == "search_user_account"
    assert response.execution_result["found"] is True
    assert response.execution_result["user"]["account_number"] == "ACC-1001"


@pytest.mark.asyncio
async def test_risky_tool_interception(test_db_session: AsyncSession):
    """Test that a risky tool (transfer_funds) is intercepted and requires HITL approval."""
    agent = AIAgent(session=test_db_session)
    response = await agent.process_chat(user_prompt="Transfer $200 from ACC-1001 to ACC-1002")

    assert response.status == "PENDING_APPROVAL"
    assert response.approval_required is True
    assert response.approval_details is not None
    assert response.approval_details["tool_name"] == "transfer_funds"

    approval_id = response.approval_details["approval_id"]

    # Verify pending approval is stored in DB
    approval = await ApprovalManager.get_approval_by_id(test_db_session, approval_id)
    assert approval is not None
    assert approval.status == "PENDING"
    assert approval.tool_args["amount"] == 200.0


@pytest.mark.asyncio
async def test_human_approval_execution_flow(test_db_session: AsyncSession):
    """Test human approval flow: approving transfer updates account balances and audit logs."""
    agent = AIAgent(session=test_db_session)
    chat_res = await agent.process_chat(user_prompt="Transfer $300 from ACC-1001 to ACC-1002")
    approval_id = chat_res.approval_details["approval_id"]

    # Process Approval response -> APPROVED
    app_res = await ApprovalManager.process_approval_response(
        session=test_db_session,
        approval_id=approval_id,
        action="APPROVED",
        responded_by="admin@test.com"
    )

    assert app_res["success"] is True
    assert app_res["status"] == "APPROVED"
    assert app_res["execution_result"]["success"] is True

    # Check updated user balances in DB
    sender = (await test_db_session.execute(select(UserAccount).where(UserAccount.account_number == "ACC-1001"))).scalars().first()
    recipient = (await test_db_session.execute(select(UserAccount).where(UserAccount.account_number == "ACC-1002"))).scalars().first()

    assert sender.balance == 700.0 # 1000 - 300
    assert recipient.balance == 800.0 # 500 + 300


@pytest.mark.asyncio
async def test_human_rejection_flow(test_db_session: AsyncSession):
    """Test human rejection flow: rejecting transfer prevents balance modification."""
    agent = AIAgent(session=test_db_session)
    chat_res = await agent.process_chat(user_prompt="Transfer $500 from ACC-1001 to ACC-1002")
    approval_id = chat_res.approval_details["approval_id"]

    # Process Approval response -> REJECTED
    app_res = await ApprovalManager.process_approval_response(
        session=test_db_session,
        approval_id=approval_id,
        action="REJECTED",
        responded_by="security@test.com",
        rejection_reason="Unusual activity pattern"
    )

    assert app_res["success"] is True
    assert app_res["status"] == "REJECTED"

    # Balances must remain unchanged
    sender = (await test_db_session.execute(select(UserAccount).where(UserAccount.account_number == "ACC-1001"))).scalars().first()
    assert sender.balance == 1000.0
