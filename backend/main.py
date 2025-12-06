import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.handler.ai_handler import router as ai_router
from app.handler.api import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 Starting TestOps-Copilot on port {settings.PORT}...")
    # Здесь можно добавить проверку соединения с БД или LLM
    yield
    print("🛑 Shutting down...")

app = FastAPI(
    title="TestOps-Copilot Backend",
    version="3.0", 
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1/ai")

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=False
    )