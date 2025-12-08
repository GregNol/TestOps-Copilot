from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Определяем путь к .env (на уровень выше папки api)
BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    SSO_GRPC_HOST: str = "localhost"
    SSO_GRPC_PORT: int = 44044
    SSO_TIMEOUT: int = 5

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore")

settings = Settings()