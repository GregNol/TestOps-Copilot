import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env файл (если есть)
load_dotenv()

class Settings:
    # Базовая директория проекта
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    RESOURCES_DIR: Path = BASE_DIR / "resources"

    # AI Настройки
    AI_MODEL_KEY: str = os.getenv("AI_MODEL_KEY", "")
    AI_MODEL_URL: str = os.getenv("AI_MODEL_URL", "")
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "Qwen/Qwen3-Coder-480B-A35B-Instruct")

    # App Settings
    HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("APP_PORT", 8080))

settings = Settings()