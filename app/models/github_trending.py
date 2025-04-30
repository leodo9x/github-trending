from pydantic import BaseModel
from typing import Optional

class GitHubTrendingItem(BaseModel):
    name: str
    link: str
    description: str
    language: Optional[str] = None
    star: str