from fastapi import FastAPI, HTTPException
from typing import List, Union, Dict
from .services.github_service import GitHubService
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
