import pytest
import httpx
import pytest_asyncio
from app.main import app
from app.services.cache_service import cache

@pytest_asyncio.fixture
async def client():
    """Create a test client for the FastAPI application."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
def clear_cache():
    """Clear cache before and after each test."""
    cache.clear_all()
    yield
    cache.clear_all()