import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_root_endpoint(client):
    """Test the root endpoint."""
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to GitHub Trending API"}

@pytest.mark.asyncio
async def test_get_github_trending(client):
    """Test the GitHub trending endpoint."""
    response = await client.get("/api/github-trending")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "code" in data
    assert "data" in data
    assert data["code"] == 200
    assert isinstance(data["data"], list)

@pytest.mark.asyncio
async def test_get_github_trending_with_since(client):
    """Test the GitHub trending endpoint with since parameter."""
    response = await client.get("/api/github-trending", params={"since": "daily"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "code" in data
    assert "data" in data
    assert data["code"] == 200
    assert isinstance(data["data"], list)

@pytest.mark.asyncio
async def test_clear_cache(client):
    """Test the clear cache endpoint."""
    response = await client.delete("/api/cache")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Cache cleared successfully"}

@pytest.mark.asyncio
async def test_clear_cache_by_date(client):
    """Test the clear cache by date endpoint."""
    date = "2024-03-20"
    response = await client.delete(f"/api/cache/{date}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": f"Cache cleared for date: {date}"}