import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.db.base import Base, get_db_session
from app.db.models import UserAccount

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_client():
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Seed sample users
    async with async_session() as session:
        u1 = UserAccount(id="usr-1", account_number="ACC-1001", full_name="Alice API", email="alice.api@test.com", balance=1000.0)
        u2 = UserAccount(id="usr-2", account_number="ACC-1002", full_name="Bob API", email="bob.api@test.com", balance=500.0)
        session.add_all([u1, u2])
        await session.commit()

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "OK"
    assert data["database"] == "HEALTHY"


@pytest.mark.asyncio
async def test_chat_safe_tool_endpoint(async_client: AsyncClient):
    payload = {"message": "Search account details for Alice API"}
    response = await async_client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "COMPLETED"
    assert data["approval_required"] is False
    assert data["tool_executed"] == "search_user_account"


@pytest.mark.asyncio
async def test_chat_and_approval_api_flow(async_client: AsyncClient):
    # 1. Trigger risky chat action
    chat_payload = {"message": "Transfer $150 from ACC-1001 to ACC-1002"}
    chat_resp = await async_client.post("/api/v1/chat", json=chat_payload)
    assert chat_resp.status_code == 200
    chat_data = chat_resp.json()

    assert chat_data["status"] == "PENDING_APPROVAL"
    assert chat_data["approval_required"] is True
    approval_id = chat_data["approval_details"]["approval_id"]

    # 2. List pending approvals
    list_resp = await async_client.get("/api/v1/approvals")
    assert list_resp.status_code == 200
    pending_list = list_resp.json()
    assert any(item["id"] == approval_id for item in pending_list)

    # 3. Approve risky action
    respond_payload = {"action": "APPROVED", "responded_by": "manager@test.com"}
    respond_resp = await async_client.post(f"/api/v1/approvals/{approval_id}/respond", json=respond_payload)
    assert respond_resp.status_code == 200
    resp_data = respond_resp.json()
    assert resp_data["status"] == "APPROVED"
    assert resp_data["execution_result"]["success"] is True


@pytest.mark.asyncio
async def test_logs_and_evaluations_endpoints(async_client: AsyncClient):
    # Run evaluations benchmark
    eval_run_resp = await async_client.post("/api/v1/evaluations/run")
    assert eval_run_resp.status_code == 200
    assert eval_run_resp.json()["status"] == "COMPLETED"

    # Get evaluation metrics
    eval_list_resp = await async_client.get("/api/v1/evaluations")
    assert eval_list_resp.status_code == 200
    metrics = eval_list_resp.json()["metrics_summary"]
    assert metrics["total_evaluations"] > 0

    # Get audit logs
    logs_resp = await async_client.get("/api/v1/logs")
    assert logs_resp.status_code == 200
    assert len(logs_resp.json()) > 0
