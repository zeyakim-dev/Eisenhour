import pytest
from fastapi.testclient import TestClient
from pytest_asyncio import fixture as pytest_asyncio_fixture
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.v1.routers.tasks import get_db
from src.core.db import Base
from src.main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest_asyncio_fixture(name="session")
async def session_fixture():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield TestingSessionLocal()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio_fixture(name="client")
async def client_fixture(session: AsyncSession):
    async def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_read_tasks(client: TestClient):
    response = client.get("/api/v1/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_task(client: TestClient):
    task_data = {"title": "새로운 할 일", "is_important": True, "is_urgent": False}
    response = client.post("/api/v1/tasks/", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["is_important"] == task_data["is_important"]
    assert created_task["is_urgent"] == task_data["is_urgent"]
    assert "id" in created_task
    assert "created_at" in created_task
    assert created_task["is_completed"] is False
