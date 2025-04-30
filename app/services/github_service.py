from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from ..config.settings import settings
from ..models.github_trending import GitHubTrendingItem
from .cache_service import cache

class GitHubService:
    def __init__(self):
        self.base_url = settings.GITHUB_TRENDING_URL
        self.timeout = settings.REQUEST_TIMEOUT
        self.max_retries = settings.MAX_RETRIES

    def _get_url(self, date: Optional[str] = None) -> str:
        url = self.base_url
        if date:
            url = f"{url}?since={date}"
        return url

    def _get_cache_key(self, date: Optional[str] = None) -> str:
        return f"github_trending:{date or 'daily'}"

    def _parse_trending_item(self, article) -> GitHubTrendingItem:
        title = article.h2
        link = f"github.com{title.a.get('href')}"
        name = title.a.text.split()[-1]

        description = ""
        if article.p:
            description = article.p.text.replace('\n', '').strip()

        language = None
        if article.find('span', itemprop="programmingLanguage"):
            language = article.find('span', itemprop="programmingLanguage").text

        star = article.find('a', class_="Link--muted").text.strip()

        return GitHubTrendingItem(
            name=name,
            link=link,
            description=description,
            language=language,
            star=star
        )

    def get_trending(self, date: Optional[str] = None) -> List[GitHubTrendingItem]:
        cache_key = self._get_cache_key(date)

        # Try to get from cache first
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data

        # If not in cache, fetch from GitHub
        url = self._get_url(date)
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                trending_items = [self._parse_trending_item(article) for article in soup.find_all('article')]

                # Cache the results
                cache.set(cache_key, trending_items)

                return trending_items
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Failed to fetch GitHub trending data after {self.max_retries} attempts: {str(e)}")
                continue