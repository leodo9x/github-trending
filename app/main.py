from fastapi import FastAPI
from .github_trending import init as github_trending_init

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/api/github-trending")
async def get_github_trending(since: str | None = None):
  github_trending = github_trending_init(since)

  return {"code": 200, "data": github_trending }
