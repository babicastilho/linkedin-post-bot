# app/tests/conftest.py
import sys
import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.database import posts_collection

# ✅ Fix for event loop compatibility on Windows with motor
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ✅ Ensure one event loop is shared across all tests
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# ✅ Optional: explicitly declare asyncio backend if using anyio (not required unless you're mixing backends)
@pytest_asyncio.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# ✅ Reusable async HTTP client with DB cleanup
@pytest_asyncio.fixture(scope="function")
async def client():
    await posts_collection.delete_many({})  # Clear DB before each test
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
