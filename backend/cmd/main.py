from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from internal import config
from internal.handler import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting application...")
    config.loadConfig()
    yield
    print("🛑 Shutting down application...")

app = FastAPI(title="TestOps-Copilot Backend",
              version="3.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("cmd.main:app", host="0.0.0.0", port=8080, reload=False)
