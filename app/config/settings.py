from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GITHUB_TRENDING_URL: str = "https://github.com/trending"
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"

settings = Settings()