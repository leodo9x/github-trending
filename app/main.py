from fastapi import FastAPI, HTTPException
from typing import List, Union, Dict
from .services.github_service import GitHubService
from .services.cache_service import cache
from .models.github_trending import GitHubTrendingItem

app = FastAPI(
    title="GitHub Trending API",
    description="API to fetch trending repositories from GitHub",
    version="1.0.0"
)

github_service = GitHubService()

@app.get("/")
async def root():
    return {"message": "Welcome to GitHub Trending API"}

@app.get("/api/github-trending")
async def get_github_trending(since: str | None = None) -> Dict[str, Union[int, List[GitHubTrendingItem]]]:
    try:
        trending_items = github_service.get_trending(since)
        return {'code': 200, 'data': trending_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/cache")
async def clear_cache():
    """Clear all cached data."""
    try:
        cache.clear_all()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/cache/{date}")
async def clear_cache_by_date(date: str):
    """Clear cache for a specific date."""
    try:
        cache_key = f"github_trending:{date}"
        cache.delete(cache_key)
        return {"message": f"Cache cleared for date: {date}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
