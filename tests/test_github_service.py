import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from app.services.github_service import GitHubService
from app.models.github_trending import GitHubTrendingItem
import requests

@pytest.fixture
def github_service():
    return GitHubService()

@pytest.fixture
def mock_html():
    return """
    <article>
        <h2><a href="/owner/repo">owner/repo</a></h2>
        <p>Test description</p>
        <span itemprop="programmingLanguage">Python</span>
        <a class="Link--muted">1,234 stars</a>
    </article>
    """

def test_get_url(github_service):
    """Test URL generation."""
    assert github_service._get_url() == github_service.base_url
    assert github_service._get_url("daily") == f"{github_service.base_url}?since=daily"

def test_get_cache_key(github_service):
    """Test cache key generation."""
    assert github_service._get_cache_key() == "github_trending:daily"
    assert github_service._get_cache_key("weekly") == "github_trending:weekly"

def test_parse_trending_item(github_service, mock_html):
    """Test parsing of trending item HTML."""
    soup = BeautifulSoup(mock_html, 'html.parser')
    article = soup.find('article')
    item = github_service._parse_trending_item(article)

    assert isinstance(item, GitHubTrendingItem)
    assert item.name == "owner/repo"
    assert item.link == "github.com/owner/repo"
    assert item.description == "Test description"
    assert item.language == "Python"
    assert item.star == "1,234 stars"

@patch('requests.get')
def test_get_trending_success(mock_get, github_service, mock_html):
    """Test successful trending data fetch."""
    mock_response = Mock()
    mock_response.content = mock_html
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    items = github_service.get_trending()
    assert isinstance(items, list)
    assert len(items) == 1
    assert isinstance(items[0], GitHubTrendingItem)

@patch('requests.get')
def test_get_trending_retry(mock_get, github_service):
    """Test retry mechanism on failure."""
    mock_get.side_effect = requests.RequestException("Connection error")

    with pytest.raises(Exception) as exc_info:
        github_service.get_trending()

    assert "Failed to fetch GitHub trending data" in str(exc_info.value)
    assert mock_get.call_count == github_service.max_retries