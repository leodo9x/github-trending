from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GITHUB_TRENDING_URL: str = "https://github.com/trending"
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    CACHE_MAX_SIZE: int = 100  # Maximum number of items to cache
    CACHE_TTL: int = 3600  # Cache time-to-live in seconds (1 hour)

    class Config:
        env_file = ".env"

settings = Settings()