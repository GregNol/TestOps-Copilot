from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    # SSO gRPC
    SSO_GRPC_HOST: str = "localhost"
    SSO_GRPC_PORT: int = 44044
    SSO_TIMEOUT: int = 5

    # LLM Service (Target for proxy)
    LLM_SERVICE_HOST: str = "llm_service"
    LLM_SERVICE_PORT: int = 8082

    # Auth
    JWT_SECRET_KEY: str  # Должен совпадать с ключом в SSO сервисе
    JWT_ALGORITHM: str = "HS256"

    @property
    def LLM_URL(self) -> str:
        return f"http://{self.LLM_SERVICE_HOST}:{self.LLM_SERVICE_PORT}"

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore")


settings = Settings()