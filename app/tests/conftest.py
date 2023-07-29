import asyncio
import json

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.users.models import User
from app.users_relationships.models import UserRelationship


@pytest.fixture(autouse=True, scope="session")
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r", encoding="UTF-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    users_relationship = open_mock_json("users_relationship")

    async with async_session_maker() as session:
        add_users = insert(User).values(users)
        add_users_relationship = insert(UserRelationship).values(users_relationship)

        await session.execute(add_users)
        await session.execute(add_users_relationship)

        await session.commit()


# Взято из документации к pytest-asyncio
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
