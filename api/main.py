import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.client import AsyncSSOClient
from api.routers import auth, proxy
from api.settings import settings

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info("🚀 Starting API Gateway...")

    # Инициализация gRPC клиента (Singleton)
    sso_client = AsyncSSOClient()
    await sso_client.connect()

    # Проверка связи с SSO
    max_retries = 10
    for i in range(max_retries):
        logger.info(f"🔄 Connecting to SSO ({i + 1}/{max_retries})...")
        is_alive = await sso_client.ping()
        if is_alive:
            logger.info("✅ SSO Service is reachable")
            break
        logger.warning(f"⚠️ SSO not ready. Retrying in 3s...")
        await asyncio.sleep(3)
    else:
        # Если цикл завершился без break
        logger.error("❌ Could not connect to SSO after multiple attempts")
    # Сохраняем клиент в state приложения
    app.state.sso_client = sso_client

    yield

    # --- Shutdown ---
    logger.info("🛑 Shutting down API Gateway...")
    await sso_client.close()


app = FastAPI(
    title="TestOps Copilot Gateway",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
# 1. Auth (gRPC)
app.include_router(auth.router, prefix="/api/v1")

# 2. AI Proxy (HTTP to Microservice)
# Обратите внимание: все запросы к /api/v1/ai/... будут требовать токен
app.include_router(proxy.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "api-gateway"}


@app.get("/api/v1/ping")
async def ping():
    """Public ping endpoint (no auth required)"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    # Исправление: указываем полный путь от корня проекта
    uvicorn.run("api.main:app", host="0.0.0.0", port=8080, reload=True)